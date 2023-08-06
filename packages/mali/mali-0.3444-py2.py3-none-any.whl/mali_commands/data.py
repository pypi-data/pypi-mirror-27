# -*- coding: utf8 -*-
import json
import os
from uuid import uuid4
from contextlib import closing
import click
import datetime
import requests
import six
from mali_commands.legit import MetadataOperationError
from tqdm import tqdm

from mali_commands.config import Config
from mali_commands.legit.dulwich import porcelain
from mali_commands.commons import add_to_data_if_not_none, output_result
from mali_commands.data_volume import create_data_volume, with_repo, default_data_volume_path, with_repo_dynamic
from mali_commands.legit.gcs_utils import do_upload
from mali_commands.legit.multi_process_control import get_multi_process_control
from mali_commands.options import data_volume_id_argument
from mali_commands.path_utils import expend_and_validate_path, get_total_files_in_path, safe_make_dirs, \
    enumerate_paths, get_batch_of_files_from_paths, safe_rm_tree, DestPathEnum


@click.group('data')
def data_commands():
    pass


def __expend_and_validate_path(path, expand_vars=True, validate_path=True, abs_path=True):
    try:
        return expend_and_validate_path(path, expand_vars, validate_path, abs_path)
    except IOError:
        click.echo('not found %s' % path, err=True)
        exit(1)


@data_commands.command('map')
@data_volume_id_argument()
@click.option('--dataPath', required=True)
@click.pass_context
def _cmd_add_data_path(ctx, volumeid, datapath):
    result = ctx.obj.handle_api(ctx.obj, requests.get, "data_volumes/{volume_id}".format(volume_id=volumeid))

    data_path = __expend_and_validate_path(datapath)

    bucket_name = result.get('bucket_name')

    params = {}
    if bucket_name is not None:
        params['object_store'] = {'bucket_name': bucket_name}

    config = create_data_volume(
        result['id'],
        data_path,
        not result['embedded'],
        result.get('display_name'),
        result.get('description'),
        **params)

    if bucket_name is None:
        config.remove_option('object_store', 'bucket_name')
        config.save()

    display_name = result.get('display_name', 'No display name provided')
    click.echo('Initialized data volume %s (%s)' % (result['id'], display_name))


@data_commands.command('create')
@click.option('--displayName', required=True)
@click.option('--description', required=False)
@click.option('--org', required=True)
@click.option('--dataPath', required=True)
@click.option('--linked/--embedded', is_flag=True, required=True)
@click.pass_context
def _cmd_create_data_volume(ctx, displayname, description, org, datapath, linked):
    data = {}

    if org == 'me':
        org = None

    add_to_data_if_not_none(data, displayname, "display_name")
    add_to_data_if_not_none(data, org, "org")
    add_to_data_if_not_none(data, description, "description")
    add_to_data_if_not_none(data, not linked, "embedded")

    expiration = ctx.obj.config.readonly_items('data_volumes').get('expiration')
    if expiration:
        data['expiration'] = expiration

    result = ctx.obj.handle_api(ctx.obj, requests.post, "data_volumes", data)

    data_volume_id = result['id']

    datapath = __expend_and_validate_path(datapath)

    create_data_volume(data_volume_id, datapath, linked, displayname, description)

    output_result(ctx, result)


@data_commands.command('config')
@data_volume_id_argument()
@click.option('--edit', is_flag=True)
@click.pass_context
def edit_config_file(ctx, volumeid, edit):
    import subprocess

    path = os.path.join(default_data_volume_path(volumeid), 'config')

    if edit:
        subprocess.call(['edit', path])
        return

    with open(path) as f:
        click.echo(f.read())


@data_commands.command('commit')
@data_volume_id_argument()
@click.option('--message', '-m', required=False)
@click.pass_context
def commit_data_volume(ctx, volumeid, message):
    with with_repo(ctx.obj.config, volumeid) as repo:
        result = repo.commit(message)

        if 'commit_id' not in result:
            click.echo('no changeset detected', err=True)
            exit(1)

        output_result(ctx, result)


def _run_add_batches(bar, repo, paths, total_files):
    def inc_bar(_):
        bar.update()

    batch_size = max(min(total_files // 100, 250), 250)  # FIXME: hardcoded

    for current_batch in get_batch_of_files_from_paths(paths, batch_size):
        porcelain.add(repo, current_batch, repo.data_volume_config.embedded, callback=inc_bar)


@data_commands.command('add')
@data_volume_id_argument()
@click.option('--files', '-f', multiple=True)
@click.option('--commit', is_flag=True, required=False)
@click.option('--message', '-m', required=False)
@click.option('--processes', default=-1, type=int, required=False)
@click.option('--no_progressbar/--enable_progressbar', default=False, is_flag=True, required=False)
@click.pass_context
def add_to_data_volume(ctx, volumeid, files, commit, message, processes, no_progressbar):
    from botocore.exceptions import NoCredentialsError

    def _validate_message_for_commit():
        if commit and not message:
            raise click.UsageError('missing --message when using --commit')

    _validate_message_for_commit()

    total_files = get_total_files_in_path(files)

    try:
        with tqdm(total=total_files, desc="Adding files", unit=' files', ncols=80, disable=no_progressbar) as bar:
            with with_repo(ctx.obj.config, volumeid) as repo:
                if processes != -1:
                    repo.data_volume_config.object_store_config['processes'] = processes

                _run_add_batches(bar, repo, files, total_files)

                if commit:
                    repo.commit(message)
    except NoCredentialsError as ex:
        click.echo('S3/boto', err=True)
        click.echo(ex.message, err=True)
        exit(1)


def __download_entity(config_init_dict, volume_id, dest_file, item):
    import google.api_core.exceptions

    config = Config(**config_init_dict)

    with with_repo(config, volume_id, read_only=True) as repo:
        try:
            _, data = repo.object_store.get_raw(item['@id'])
        except requests.exceptions.HTTPError as ex:
            if ex.response.status_code == 404:
                return

            raise
        except google.api_core.exceptions.NotFound:
            return

        safe_make_dirs(os.path.dirname(dest_file))

        json_metadata_name = dest_file + '.metadata.json'

        with open(json_metadata_name, 'w') as metadata_file:
            json.dump(item, metadata_file)

        def append_id(filename, uid):
            name, ext = os.path.splitext(filename)
            return "{name}_{uid}{ext}".format(name=name, uid=uid, ext=ext)

        if os.path.exists(dest_file):
            dest_file = append_id(dest_file, item['@id'])

        with open(dest_file, 'wb') as f:
            f.write(data)


@data_commands.command('clone')
@data_volume_id_argument()
@click.option('--dest', '-d', required=True)
@click.option('--query', '-q', required=False)
@click.option('--delete', is_flag=True, required=False)
@click.option('--batchSize', required=False, default=500)
@click.option('--processes', default=-1, type=int, required=False)
@click.option('--no_progressbar/--enable_progressbar', default=False, is_flag=True, required=False)
@click.pass_context
def clone_data(ctx, volumeid, dest, query, delete, batchsize, processes, no_progressbar):
    if delete and (dest in ('.', './', '/', os.path.expanduser('~'), '~', '~/')):
        raise click.BadParameter("for protection --dest can't point into current directory while using delete")

    dest = os.path.abspath(__expend_and_validate_path(dest, expand_vars=False, validate_path=False))

    root_dest = DestPathEnum.find_root(dest)

    if delete:
        safe_rm_tree(root_dest)

    def get_next_results(start_index):
        current_results, current_total_data_points = repo.metadata.query(query, max_results=batchsize, start_index=start_index)

        return list(current_results), current_total_data_points

    phase_meta = {}

    def download_all(current_results):
        start_index = 0

        results = current_results

        while True:
            for item in results:
                item = normalize_item(item)
                config_init_dict = ctx.obj.config.init_dict

                phase = item.get('@phase', 'all')

                full_path = DestPathEnum.get_full_path(dest, item)

                path = os.path.relpath(full_path, root_dest)
                phase_meta.setdefault(phase, {})[path] = item

                multi_process_control.execute(
                    __download_entity, args=(config_init_dict, volumeid, full_path, item), callback=lambda _: bar.update())

            if len(results) != batchsize:
                break

            start_index += len(results)

            results, _ = get_next_results(start_index)

        return phase_meta

    multi_process_control = get_multi_process_control(processes)

    try:
        safe_make_dirs(root_dest)

        with with_repo_dynamic(ctx, volumeid) as repo:
            begin_results, total_data_points = get_next_results(0)

            with tqdm(total=total_data_points, desc="Downloading", unit=' data point', ncols=80, disable=no_progressbar) as bar:
                with closing(multi_process_control):
                    try:
                        phase_meta = download_all(begin_results)
                    except MetadataOperationError as ex:
                        click.echo(ex.message, err=True)
                        exit(1)
                        return

            with tqdm(total=len(phase_meta), desc="saving metadata", unit=' files', ncols=80, disable=no_progressbar) as bar:
                for key, val in phase_meta.items():
                    json_metadata_file = os.path.join(root_dest, key + '.metadata.json')

                    with open(json_metadata_file, 'w') as f:
                        json.dump(val, f)

                    bar.update()

    except KeyboardInterrupt:
        multi_process_control.terminate()
        multi_process_control.close()


@data_commands.group('metadata')
def metadata_commands():
    pass


def stats_from_json(now, json):
    return os.stat_result((
        0,  # mode
        0,  # inode
        0,  # device
        0,  # hard links
        0,  # owner uid
        0,  # gid
        len(json),  # size
        0,  # atime
        now,
        now,
    ))


def normalize_item(item):
    result_item = {}

    for key, val in item.items():
        if key == 'meta':
            continue

        result_item['@' + key] = val

    for key, val in item.get('meta', {}).items():
        result_item[key] = val

    return result_item


@data_commands.command('query')
@data_volume_id_argument()
@click.option('--query', '-q')
@click.option('--batchSize', required=False, default=500)
@click.pass_context
def query_metadata(ctx, volumeid, query, batchsize):
    def get_all_results():
        def get_next_results():
            current_results, current_total_data_points = repo.metadata.query(
                query, max_results=batchsize, start_index=start_index)

            return list(current_results), current_total_data_points

        total_results = []

        start_index = 0

        results, total_data_points = get_next_results()
        while True:
            total_results.extend([normalize_item(item) for item in results])

            if len(results) != batchsize:
                break

            start_index += len(results)

            results, total_data_points = get_next_results()

        return total_results

    try:
        with with_repo_dynamic(ctx, volumeid) as repo:
            all_results = get_all_results()
    except MetadataOperationError as ex:
        click.echo(ex.message, err=True)
        exit(1)
        return

    output_result(ctx, all_results)


def chunks(l, n):
    result = []
    for item in l:
        result.append(item)

        if len(result) == n:
            yield result
            result = []

    if result:
        yield result


def __json_data_from_files(data_path, files, data_per_entry):
    def rel_path_if_needed(path):
        if os.path.isabs(path):
            return os.path.relpath(path, data_path)

        return path

    for file_path in enumerate_paths(files):
        file_path = rel_path_if_needed(file_path)
        yield file_path, data_per_entry


def validate_json(ctx, param, value):
    try:
        if value is None:
            return None

        return json.loads(value)
    except ValueError:
        raise click.BadParameter('not valid json', param=param, ctx=ctx)


def __multi_line_json_from_data(data):
    def items():
        if isinstance(data, dict):
            for key, val in data.items():
                val['_sha'] = key

                yield val
        else:  # list, generators
            for key, val in data:
                val['_sha'] = key

                yield val

    result = six.BytesIO()
    for i, item in enumerate(items()):
        json_str = json.dumps(item) + '\n'
        result.write(json_str.encode())

    return result


class File2(click.File):
    def convert(self, value, param, ctx):
        value = os.path.expanduser(value)

        return super(File2, self).convert(value, param, ctx)


def __newline_json_file_from_json_file(datafile):
    json_data = json.load(datafile)
    return __multi_line_json_from_data(json_data)


def __repo_validate_data_path(repo, volume_id):
    if repo.data_path:
        return

    msg = 'Data volume {0} was not mapped on this machine, ' \
          'you should call "mali data map {0} --dataPath [root path of data]" ' \
          'in order to work with the volume locally'.format(volume_id)
    click.echo(msg, err=True)
    exit(1)


@metadata_commands.command('add')
@data_volume_id_argument()
@click.option('--files', '-f', multiple=True)
@click.option('--data', '-d', required=False, callback=validate_json)
@click.option('--dataPoint', '-dp', multiple=True)
@click.option('--dataFile', '-df', required=False, type=File2())
@click.option('--property', '-p', required=False, type=(str, str), multiple=True)
@click.option('--propertyInt', '-pi', required=False, type=(str, int), multiple=True)
@click.option('--propertyFloat', '-pf', required=False, type=(str, float), multiple=True)
@click.option('--update/--replace', is_flag=True, default=True, required=False)
@click.option('--no_progressbar/--enable_progressbar', default=False, is_flag=True, required=False)
@click.pass_context
def add_to_metadata(
        ctx, volumeid, files, data, datapoint, datafile, property, propertyint, propertyfloat, update, no_progressbar):

    def get_per_data_entry():
        data_per_entry = data or {}

        for props in (property, propertyint, propertyfloat):
            if not props:
                continue

            for prop_name, prop_val in props:
                data_per_entry[prop_name] = prop_val

        return data_per_entry

    require_map = files is not None

    def get_current_data_file():
        if datafile:
            return __newline_json_file_from_json_file(datafile)

        entries = datapoint or []
        entries.extend(files or [])

        __repo_validate_data_path(repo, volumeid)

        data_list = __json_data_from_files(repo.data_path, entries, get_per_data_entry())

        return __multi_line_json_from_data(data_list)

    def upload_file_for_processing():
        data_object_name = '%s/temp/%s.json' % (volumeid, uuid4().hex)

        url = 'data_volumes/{volume_id}/gcs_urls'.format(volume_id=volumeid)

        headers = {'Content-Type': 'application/json'}

        msg = {
            'methods': 'PUT',
            'paths': [data_object_name],
            'content_type': 'application/json'
        }

        result = ctx.obj.handle_api(ctx.obj, requests.post, url, msg)

        put_url = result['put'][0]

        file_obj = get_current_data_file()

        with tqdm(total=file_obj.tell(), desc="Uploading", unit=' KB', ncols=80, disable=no_progressbar, unit_scale=True) as bar:
            do_upload(gcs_auth, None, data_object_name, file_obj, headers, head_url=None, put_url=put_url, callback=lambda c: bar.update(c))

        return data_object_name

    with with_repo(ctx.obj.config, volumeid, require_map=require_map) as repo:
        gcs_auth = repo.data_volume_config.object_store_config.get('auth')

        metadata = repo.metadata

        object_name = upload_file_for_processing()

        start_time = datetime.datetime.utcnow()
        click.echo('Processing Metadata')
        metadata.add_data(data='gs://' + object_name)
        click.echo('Processing Done (%s)' % (datetime.datetime.utcnow() - start_time))


@data_commands.command('list')
@click.pass_context
def list_data_volumes(ctx):
    projects = ctx.obj.handle_api(ctx.obj, requests.get, 'data_volumes')

    output_result(ctx, projects.get('volumes', []), ['id', 'display_name', 'description', 'org'])
