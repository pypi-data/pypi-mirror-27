# -*- coding: utf8 -*-
import os
import json
from filecmp import dircmp

from datetime import datetime
from click.testing import CliRunner

from tests.base import BaseCliTest, global_some_random_shit
from mali import cli
from mali_commands.utilities.os_utils import create_dir
from mali_commands.utilities.list_utils import flatten


MALI_INTEGRATION_SERVER_ENV = os.environ.get('MALI_INTEGRATION_SERVER_ENV', 'staging').lower()
MALI_CONFIG_PREFIX = 'test-%s' % MALI_INTEGRATION_SERVER_ENV
MALI_CONFIG_FILENAME = '%s-missinglink.cfg' % MALI_CONFIG_PREFIX

IGNORED_FILES = [
    '.DS_Store',
    'test-staging-missinglink.cfg',
    'test-prod-missinglink.cfg',
]


def create_file(filename, content=None):
    dirname = os.path.dirname(filename)

    create_dir(dirname)

    content = content or global_some_random_shit(size=1024 * 4)
    with open(filename, 'w') as f:
        f.write(content)


class BaseTest(BaseCliTest):
    def setUp(self):
        super(BaseTest, self).setUp()
        self.runner = CliRunner()

        # We create `./temp/<time_stamp>` for creating temporary data files and cloning.
        # '<time_stamp>' uniqueness allows tests to run in parallel without corrupting each other's data.
        # It will be deleted on `tearDown`.
        # Under `./temp/<time_stamp>`, there are:
        # - `data` which contains data files used for committing
        # - `clone` which can be use to clone the data volume
        # Data manipulation (e.g. filenames) are relative to `./temp/<time_stamp>/data`
        self.test_root_dir = os.getcwd()
        self.temp_dir = os.path.join(self.test_root_dir, 'temp', datetime.utcnow().isoformat())
        self.data_dir = os.path.join(self.temp_dir, 'data')
        self.clone_dir = os.path.join(self.temp_dir, 'cloned')

        create_dir(self.data_dir)

    def tearDown(self):
        super(BaseTest, self).tearDown()

        # remove_dir(self.temp_dir)

    @classmethod
    def log_stage(cls, fmt, *args, **kwargs):
        import sys

        err = kwargs.get('err', False)
        file_output = sys.stderr if err else sys.stdout
        file_output.write(fmt % args + '\n')

    def populate_data(self, filenames, contents=None):
        filenames = self._filenames_with_data_path(filenames)
        contents = contents or [None] * len(filenames)

        for filename, content in zip(filenames, contents):
            path = os.path.join(filename)
            create_file(path, content)

    def create_data_volume(self, display_name='TestVolume', org='me', data_path=None):
        data_path = data_path or self.data_dir
        self.log_stage("Creating data volume with display name = '%s', org = '%s', data_path = '%s' ...", display_name, org, data_path)

        result = self._run_command([
            'data', 'create',
            '--displayName', display_name,
            '--org', org,
            '--dataPath', data_path
        ])
        return json.loads(result.output)['id']

    def add_file(self, volume_id, filenames, processes=1):
        filenames = self._filenames_with_data_path(filenames)
        self.log_stage('In volume %s, adding files: %s ...', volume_id, filenames)

        args = ['data', 'add', volume_id]
        args.extend(self._multiple_options_to_args('--files', filenames))
        args.append('--no_progressbar')

        if processes is not None:
            args.extend(['--processes', str(processes)])

        return self._run_command(args)

    def add_metadata(self, volume_id, filenames, metadata):
        filenames = self._filenames_with_data_path(filenames)
        self.log_stage('In volume %s, adding metadata %s to files: %s ...', volume_id, metadata, filenames)

        args = ['data', 'metadata', 'add', volume_id]
        args.extend(self._multiple_options_to_args('--files', filenames))
        args.extend(['--data', json.dumps(metadata)])
        args.append('--no_progressbar')
        return self._run_command(args)

    def commit(self, volume_id, message=''):
        self.log_stage('In volume %s, committing: %s ...', volume_id, message)

        result = self._run_command([
            'data', 'commit', volume_id,
            '--message', message
        ])
        return json.loads(result.output)

    def query(self, volume_id, query):
        self.log_stage('In volume %s, query: %s ...', volume_id, query)

        result = self._run_command([
            'data', 'query', volume_id,
            '--query', query
        ])
        return json.loads(result.output)

    def clone(self, volume_id, dest, query, processes=1):
        self.log_stage("Cloning volume %s, with query '%s' ...", volume_id, query)

        args = [
            'data', 'clone', volume_id,
            '--dest', dest,
            '--query', query,
            '--no_progressbar'
        ]

        if processes is not None:
            args.extend(['--processes', str(processes)])

        return self._run_command(args)

    def _filenames_with_data_path(self, filenames):
        return [os.path.join(self.data_dir, filename) for filename in filenames]

    @classmethod
    def _multiple_options_to_args(cls, option_name, option_values):
        return flatten(zip([option_name] * len(option_values), option_values))

    def _run_command(self, command_args, should_assert=True):
        cmd_start_time = datetime.utcnow()

        config_file = '%s.cfg' % MALI_CONFIG_PREFIX
        config_abs_file = os.path.join(os.path.dirname(__file__), 'config', config_file)

        mali_test_args = [
            '--outputFormat', 'json',
            '--configFile', config_abs_file,
        ]
        args = mali_test_args + command_args
        result = self.runner.invoke(cli, args, catch_exceptions=False)

        self.log_stage('Command run: %s', ' '.join(['mali'] + args), err=result.exit_code != 0)
        self.log_stage(
            'Command status: %d, output: %s, took: %s',
            result.exit_code, result.output, datetime.utcnow() - cmd_start_time, err=result.exit_code != 0)

        if should_assert:
            self.assertEqual(result.exit_code, 0, 'run command %s failed' % command_args)

        return result

    def assertEqualDir(self, dir1, dir2):
        dir_diff = dircmp(dir1, dir2, ignore=IGNORED_FILES)
        self._assertEqualDirRecursively(dir_diff)

    def _assertEqualDirRecursively(self, dir_diff):
        if dir_diff.left_only:
            dir_diff.left_only.sort()
            msg = 'Only in %s: %s' % (dir_diff.left, dir_diff.left_only)
            self._raiseDirDiffException(dir_diff, msg)

        if dir_diff.right_only:
            dir_diff.right_only.sort()
            msg = 'Only in %s: %s' % (dir_diff.right, dir_diff.right_only)
            self._raiseDirDiffException(dir_diff, msg)

        if dir_diff.diff_files:
            dir_diff.diff_files.sort()
            msg = 'Differing files: %s' % dir_diff.diff_files
            self._raiseDirDiffException(dir_diff, msg)

        if dir_diff.common_funny:
            dir_diff.common_funny.sort()
            msg = 'Common funny cases: %s' % dir_diff.common_funny
            self._raiseDirDiffException(dir_diff, msg)

        if dir_diff.funny_files:
            dir_diff.funny_files.sort()
            msg = 'Trouble with common files: %s' % dir_diff.funny_files
            self._raiseDirDiffException(dir_diff, msg)

        for subdir, subdir_diff in dir_diff.subdirs.items():
            self._assertEqualDirRecursively(subdir_diff)

    def _raiseDirDiffException(self, dir_diff, msg):
        msg = "Diffing '%s' and '%s'...\n%s" % (dir_diff.left, dir_diff.right, msg)
        raise self.failureException(msg)
