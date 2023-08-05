# -*- coding: utf8 -*-
from pprint import pprint

import click
import requests
from click import exceptions

from mali_commands.commons import output_result


@click.group('cluster')
def cluster_commands():
    pass


@cluster_commands.command('add')
@click.pass_context
@click.option('--default', type=bool, help='Set this cluster as the default cluster', default=True)
@click.option('--alias', type=str, required=False, help='Alias for this cluster. By default, the cluster id will be used.')
@click.option('--url', type=str, required=True, help='The configuration url of the cluster')
def add_cluster(ctx, default, alias, url):
    # try:
    if alias is not None and alias is 'default':
        raise exceptions.BadOptionUsage('alias can not be "default". Please use --default flag instead')

    cluster_info = requests.request('GET', url).json()
    pprint(cluster_info)

    add_id = alias or cluster_info['id']
    cluster_id = '{}_{}'.format('cluster', add_id)
    ctx.obj.config.update_and_save({
        cluster_id: cluster_info
    })
    print("Cluster {} added.".format(add_id))

    clusters = ctx.obj.config.clusters
    clusters[add_id] = cluster_id
    if default:
        clusters['default'] = cluster_id
    ctx.obj.config.update_and_save({
        'clusters': clusters
    })


@cluster_commands.command('list')
@click.pass_context
@click.option('--outputFormat', '-o', type=click.Choice(['tables', 'json']), default='tables', required=False)
def list_clusters(ctx, outputformat):
    ctx.obj.bad_json_format = outputformat == 'json'
    data = []
    clusters = ctx.obj.config.clusters
    default_cluster = clusters.get('default')
    for cluster_name in clusters:
        if cluster_name == 'default':
            continue
        claster_id = clusters[cluster_name]
        cluster = ctx.obj.config.cluster(claster_id)
        cluster['alias'] = cluster_name
        cluster['default'] = default_cluster == claster_id
        data.append(cluster)
    output_result(ctx, data, ['alias', 'id', 'config_url', 'default'])


@cluster_commands.command('remove')
@click.argument('alias', type=str, required=True)
@click.pass_context
def remote_cluster(ctx, alias):
    clusters = ctx.obj.config.clusters
    default_cluster = clusters.get('default')
    rem_cluser = clusters.get(alias)
    if rem_cluser is None:
        raise exceptions.BadOptionUsage('Could not find cluster with id {}'.format(alias))
    if rem_cluser == default_cluster:
        raise exceptions.BadOptionUsage('{} is the default cluster. Please change the default cluster first by calling `mali cluster default <new_default>'.format(alias))
    del (clusters[alias])

    # TODO: delete the cluster section as well
    ctx.obj.config.update_and_save({
        'clusters': clusters
    })
    print('Cluster {} removed'.format(alias))


@cluster_commands.command('default')
@click.argument('alias', type=str, required=True)
@click.pass_context
def default_cluster(ctx, alias):
    clusters = ctx.obj.config.clusters
    rem_cluser = clusters.get(alias)
    if rem_cluser is None:
        raise exceptions.BadOptionUsage('Could not find cluster with id {}'.format(alias))
    clusters['default'] = alias
    # TODO: delete the cluster section as well
    ctx.obj.config.update_and_save({
        'clusters': clusters
    })
    print('Cluster {} is now default'.format(alias))
