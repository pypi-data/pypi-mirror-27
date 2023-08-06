# -*- coding: utf8 -*-
import glob
import os
import shutil
import errno

ignore_files = ['.DS_Store']


def enumerate_path(path):
    path = expend_and_validate_path(path)
    if is_glob(path):
        for path in glob.glob(path):
            yield path

        return

    if os.path.isfile(path):
        yield path
        return

    if os.path.isdir(path):
        for root, dirs, files in os.walk(path, followlinks=True):
            for file_ in files:
                if file_ in ignore_files:
                    continue

                yield os.path.join(root, file_)


def enumerate_paths(paths):
    for path in paths:
        for file_ in enumerate_path(path):
            yield file_


def get_total_files_in_path(paths):
    total_files = 0
    for _ in enumerate_paths(paths):
        total_files += 1

    return total_files


def is_glob(path):
    return '*' in path or '?' in path


def expend_and_validate_path(path, expand_vars=True, validate_path=True, abs_path=True):
    path = os.path.expanduser(path)

    if expand_vars:
        path = os.path.expandvars(path)

    if abs_path:
        path = os.path.abspath(path)

    if not is_glob(path) and validate_path and not os.path.exists(path):
        raise IOError()

    return path


def get_batch_of_files_from_paths(paths, batch_size):
    batch = []
    for file_or_path in enumerate_paths(paths):
        batch.append(file_or_path)
        if len(batch) == batch_size:
            yield batch
            batch = []

    if len(batch) > 0:
        yield batch


def fill_in_vars(path, replace_vars):
    replace_vars_keys = sorted(replace_vars.keys(), reverse=True)

    for var_name in replace_vars_keys:
        var_value = replace_vars[var_name]
        path = path.replace('$' + var_name, str(var_value))
        path = path.replace('#' + var_name, str(var_value))

    return path


def safe_make_dirs(dir_name):
    try:
        os.makedirs(dir_name)
    except OSError as ex:
        if ex.errno != errno.EEXIST:
            raise


def path_elements(path):
    folders = []
    while 1:
        path, folder = os.path.split(path)

        if folder != "":
            folders.append(folder)
        else:
            if path != "":
                folders.append(path)

            break

    folders.reverse()

    return folders


def safe_rm_tree(path):
    try:
        shutil.rmtree(path)
    except OSError as ex:
        if ex.errno != errno.ENOENT:
            raise


def add_sys_var(name, value, current_vars):
    current_vars['@' + name] = value

    if name not in current_vars:
        current_vars[name] = value


def sys_vars_in_path(path, names):
    for name in names:
        if name.startswith('$'):
            if name in path:
                return True

            continue

        if '$' + name in path:
            return True

        if '$@' + name in path:
            return True

    return False
