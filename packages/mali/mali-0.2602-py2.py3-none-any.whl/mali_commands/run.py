# -*- coding: utf8 -*-
import os
import shutil
import uuid

import click
import requests
import yaml
from click import exceptions


@click.group('run', help='runs an experiment on a cluster. By defaults run on a local cluster ')
def run_commands():
    pass


def _load_recipe(r_path):
    if not os.path.isfile(r_path):
        return {}
    else:
        print('loading defaults from recipe: %s', r_path)
        with open(r_path) as f:
            return yaml.load(f)


run_options = ['cluster', 'image', 'data-dir', 'output-dir', 'source-dir', 'command']
DEFAULT_RECIPE_PATH = '.ml_recipe'


@run_commands.command('xp')
@click.pass_context
@click.option('--cluster', type=str, help='Target cluster_id, defaults to `default`')
@click.option('--image', type=str, required=False, help='Docker image to use, defaults to keras 1.2.2 (gw000)')
@click.option('--data-dir', type=str, required=False, help='data directory for the experiment. will be available as "/data" from within the experiment')
@click.option('--output-dir', type=str, required=False, help='output directory for the experiment. will be available as "/output" from within the experiment')
@click.option('--source-dir', type=str, required=False, help='output directory for the experiment. will be available as "/source" from within the experiment')
@click.option('--command', type=str, required=False, help='command to execute')
@click.option('--data-volume', type=str, required=False, help='data volume to clone data from')
@click.option('--data-query', type=str, required=False, help='query to execute on the data volume')
@click.option('--recipe', '-r', type=str, required=False, help='recipe file. recipe file is yaml file with the `flag: value` that allows you to specify default values for all params for this function')
@click.option('--save-recipe', type=str, required=False, help='Saves a recipe for this call to the target file and quits. Note the default values are not encoded into the recipe')
def add_cluster(ctx, cluster, image, data_dir, output_dir, source_dir, command, data_query, data_volume, recipe, save_recipe):
    # try:

    input_data = {
        'cluster': cluster,
        'image': image,
        'data-dir': data_dir,
        'output-dir': output_dir,
        'source-dir': source_dir,
        'command': command,
        'data-query': data_query,
        'data-volume': data_volume}
    recipe_data = _load_recipe(recipe or DEFAULT_RECIPE_PATH)
    input_data.update(recipe_data)
    if save_recipe is not None:
        with open(save_recipe, 'w') as f:
            yaml.dump(input_data, f, default_flow_style=False)
            print('Configuration saved to ', save_recipe)
        return

    if input_data.get('image') is None and input_data.get('command') is None:
        raise exceptions.BadOptionUsage('No command nor image provided')

    # apply defaults:
    input_data['image'] = input_data.get('image') or 'gw000/keras:1.2.2-cpu'
    input_data['cluster'] = input_data.get('cluster') or 'default'

    cl = ctx.obj.config.cluster_by_name(input_data['cluster'])
    if cl is None:
        raise exceptions.BadOptionUsage('Cluster {} not found'.format(cluster))

    # todo: start experiment here. get the exp id, get the remote logger.
    exp_id = uuid.uuid4().hex
    default_exp_dir = os.path.join(cl['submit_dir'], exp_id)
    input_data['source-dir'] = input_data.get('source-dir') or os.getcwd()
    os.mkdir(default_exp_dir)

    if input_data.get('data-dir') is None:
        input_data['data-dir'] = os.path.join(default_exp_dir, 'data')
        os.mkdir(input_data['data-dir'])
    if input_data.get('output-dir') is None:
        input_data['output-dir'] = os.path.join(default_exp_dir, 'output')
        os.mkdir(input_data['output-dir'])

    # todo better handling of ingnoring
    target_source_dir = os.path.join(default_exp_dir, 'source')
    print("Copying source directory. to {}".format(target_source_dir))
    shutil.copytree(input_data['source-dir'], target_source_dir, ignore=shutil.ignore_patterns('.*'))
    print("done Copying source directory")
    data = {
        "img": input_data['image'],
        "command": "bash -c '{}'".format(input_data['command']),
        "code": target_source_dir,
        "data": input_data['data-dir'],
        "output": input_data['output-dir'],
    }

    print("Start experiment")
    submit_url = cl['config_url'].replace('/config/', '/experiment/run')
    with requests.post(submit_url, json=data, stream=True) as r:
        for line in r.iter_lines(decode_unicode=True):
            line = line.strip().replace('\b', '')
            if len(line) == 0:
                continue
            print(line)
