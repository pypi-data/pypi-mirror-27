# -*- coding: utf8 -*-
import datetime
import logging
from ..bigquery_mixin import BigQueryMixin, BqJob
from .base_db_index import BaseMLIndex
from .cache import DatastoreTreeCache, GAEDatastoreTreeCache
from ..db import DatastoreConnection, GAEDatastoreConnection


# noinspection SqlNoDataSourceInspection,SqlResolve
class BigQueryMLIndex(BaseMLIndex, BigQueryMixin):
    STAGING_INDEX_TABLE_NAME = 'staging_index'
    INDEX_TABLE_NAME = 'index'

    def __init__(self, connection, version=None, delete_temp_on_commit=True):
        self.__version = version or 0

        super(BigQueryMLIndex, self).__init__(connection)
        self.__delete_temp_on_commit = delete_temp_on_commit
        self.__create_tree_cache(connection)

    def __create_tree_cache(self, connection):
        if GAEDatastoreTreeCache is not None:
            org_id = self._connection.data_volume_config.org
            volume_id = self._connection.data_volume_config.volume_id

            tree_cache = GAEDatastoreTreeCache(org_id, volume_id)
        else:
            datastore_connection = DatastoreConnection(connection.data_volume_config, connection.project)
            tree_cache = DatastoreTreeCache(datastore_connection)

        self.__tree_cache = tree_cache

    def __get_index_table_ref(self):
        return self._get_table_ref(self.INDEX_TABLE_NAME)

    def __get_staging_index_table_ref(self):
        staging_table_name = '%s_%s' % (self.STAGING_INDEX_TABLE_NAME, self.__version)
        return self._get_table_ref(staging_table_name)

    def __query_count_metadata_and_data_point(self, query):
        from google.cloud.bigquery import QueryJobConfig

        job_config = QueryJobConfig()

        job = self._query_async(query, job_config)

        def process_result(result):
            rows_iter = list(result)
            result = {}
            for is_meta, count in rows_iter:
                field = 'total_meta_data' if is_meta else 'total_data_points'
                result[field] = count

            return result.get('total_data_points', 0), result.get('total_meta_data', 0)

        return BqJob(job, process_result)

    def rpc_version_count_items(self):
        with self._connection.get_cursor() as bq_dataset:
            query = """
                #standardSQL
                SELECT ANY_VALUE(ENDS_WITH(name, '.metadata')), COUNT(DISTINCT name) 
                FROM (SELECT DISTINCT name
                  FROM `{dataset_name}.{index_table_name}`
                  UNION ALL
                    SELECT DISTINCT name
                    FROM `{dataset_name}.{staging_index_table_name}`
                )
                GROUP BY ENDS_WITH(name, '.metadata')
                """.format(
                    dataset_name=bq_dataset.dataset_id,
                    staging_index_table_name=self.__get_staging_index_table_ref().table_id,
                    index_table_name=self.__get_index_table_ref().table_id
            )

            return self.__query_count_metadata_and_data_point(query)

    def rpc_staging_count_items(self):
        staging_table_ref = self.__get_staging_index_table_ref()
        staging_index_table_full_name = staging_table_ref.table_id

        with self._connection.get_cursor() as bq_dataset:
            query = """
                #standardSQL
                SELECT ANY_VALUE(ENDS_WITH(name, '.metadata')), COUNT(DISTINCT name)
                FROM {dataset_name}.{staging_index_table_full_name}
                GROUP BY ENDS_WITH(name, '.metadata')
                """.format(
                    dataset_name=bq_dataset.dataset_id,
                    staging_index_table_full_name=staging_index_table_full_name)

            return self.__query_count_metadata_and_data_point(query)

    @classmethod
    def __table_schema(cls):
        from google.cloud import bigquery

        schema = (
            bigquery.SchemaField('name', 'STRING', 'REQUIRED'),
            bigquery.SchemaField('sha', 'STRING', 'REQUIRED'),
            bigquery.SchemaField('ctime', 'FLOAT', 'REQUIRED'),
            bigquery.SchemaField('mtime', 'FLOAT', 'REQUIRED'),
            bigquery.SchemaField('mode', 'INTEGER', 'REQUIRED'),
            bigquery.SchemaField('size', 'INTEGER', 'REQUIRED'),
            bigquery.SchemaField('url', 'STRING'),
            bigquery.SchemaField('commit_sha', 'STRING', 'REQUIRED'),  # this has to be the last column
            bigquery.SchemaField('ts', 'TIMESTAMP', 'REQUIRED'),  # this has to be the last column
        )

        return schema

    def _create_table_if_needed(self):
        import google.cloud.exceptions
        from google.cloud.bigquery.table import Table

        bq_client = self._connection

        def create_table(method):
            index_table_ref = method()

            table = Table(index_table_ref)
            table.schema = self.__table_schema()

            try:
                bq_client.update_table(table, ['schema'])
            except google.cloud.exceptions.NotFound:
                try:
                    bq_client.create_table(table)
                except google.cloud.exceptions.Conflict:
                    pass

            return table

        create_table(self.__get_index_table_ref)
        create_table(self.__get_staging_index_table_ref)

    def set_entries(self, entries):
        if not entries:
            return

        now = datetime.datetime.utcnow()

        def decode_row_without_gid_uid(entries):
            for name, sha, ctime, mtime, mode, _, _, size, url in self._decode_entries(entries):
                yield name, sha, ctime, mtime, mode, size, url, 'staging', now

        rows = [row for row in decode_row_without_gid_uid(entries)]

        logging.debug('inserting %s rows into bq', len(rows))

        index_table_ref = self.__get_staging_index_table_ref()

        bq_client = self._connection

        bq_client.create_rows(index_table_ref, rows, selected_fields=self.__table_schema())

        self.__tree_cache.set_entries(entries)

        logging.debug('inserted %s rows into bq', len(rows))

    def get_commit_id(self):
        return self.__tree_cache.get_commit_id()

    def __truncate_staging(self):
        if not self.__delete_temp_on_commit:
            logging.debug('index: delete_temp_on_commit: False')
            return

        logging.info('truncate index staging')

        staging_table_ref = self.__get_staging_index_table_ref()
        bq_client = self._connection
        bq_client.delete_table(staging_table_ref)

    def begin_commit(self, commit_sha, tree_id, ts):
        from google.cloud import bigquery

        bq_client = self._connection

        staging_index_table_ref = self.__get_staging_index_table_ref()
        index_table_ref = self.__get_index_table_ref()

        with bq_client.get_cursor() as bq_dataset:
            src_query = """
                #standardSQL
                SELECT staging_index_table.*, @commit_sha as commit_sha, @ts as ts 
                FROM (
                    SELECT * EXCEPT(row_number, ts, commit_sha)
                    FROM (
                      SELECT *, ROW_NUMBER() OVER (PARTITION BY name) row_number
                      FROM `{dataset_name}.{staging_index_table_ref}`
                    )
                    WHERE row_number = 1
                ) staging_index_table
                LEFT JOIN `{dataset_name}.{index_table_name}` index_table
                ON staging_index_table.sha = index_table.sha AND staging_index_table.name = index_table.name
                WHERE index_table.sha is NULL
              """.format(
                dataset_name=bq_dataset.dataset_id,
                staging_index_table_ref=staging_index_table_ref.table_id,
                index_table_name=index_table_ref.table_id,
            )

            src_query_parameters = (
                bigquery.ScalarQueryParameter('commit_sha', 'STRING', commit_sha),
                bigquery.ScalarQueryParameter('ts', 'TIMESTAMP', ts),
            )

            job = self._async_copy_table_data(
                src_query, src_query_parameters, self.__get_index_table_ref())

            return BqJob(job)

    def end_commit(self):
        self.__truncate_staging()

    def delete_all(self):
        self.__tree_cache.delete_all()

        index_table = self._get_table_name(self._connection.table_prefix, self.INDEX_TABLE_NAME)
        staging_index_table_prefix = self._get_table_name(self._connection.table_prefix, self.STAGING_INDEX_TABLE_NAME)
        self._connection.delete_tables([index_table, staging_index_table_prefix])
