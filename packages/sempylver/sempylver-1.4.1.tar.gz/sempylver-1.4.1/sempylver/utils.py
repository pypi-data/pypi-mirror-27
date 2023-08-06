import yaml
from shutil import copyfileobj
from os.path import join, basename, isfile
from sempylver.constants import global_config, this_dir,\
    setup_file_replacement_string, version_regex, version_pattern,\
    replace_newlines_base, has_import_regex
from re import sub
import subprocess


class config_parser(object):

    def __init__(
        self,
        config_file=global_config
    ):
        #
        # Set destination for config file
        self.config_file = config_file
        #
        # Parse config yml
        with open(config_file, 'r') as cf:
            config_opts_string = cf.read()
            self.config_opts = yaml.load(config_opts_string)
        #
        return

    def set(
        self,
        config_name,
        value,
    ):
        #
        # Set config dict value
        self.config_opts[config_name] = value
        #
        return self

    def write(self):
        with open(self.config_file, 'w') as cf:
            yaml.dump(self.config_opts, cf, default_flow_style=False)
        #
        return


def copy_with_newlines(orig_dir, tgt_dir, file_name, use_unix_newlines=False):
    #
    orig_file_name = join(orig_dir, file_name)
    tgt_file_name = join(tgt_dir, file_name)
    with open(orig_file_name, 'r') as orig_file:
        #
        with open(tgt_file_name, 'w') as tgt_file:
            copyfileobj(orig_file, tgt_file)
        #
    #
    if use_unix_newlines:
        replace_newlines_cmd = replace_newlines_base + tgt_file_name
        subprocess.call(replace_newlines_cmd)
    #
    return

def write_hooks(git_hook_directory):
    #
    copy_with_newlines(this_dir, git_hook_directory, 'commit-msg', use_unix_newlines=True)
    copy_with_newlines(this_dir, git_hook_directory, 'commit_msg.py')
    copy_with_newlines(this_dir, git_hook_directory, 'post-commit', use_unix_newlines=True)
    copy_with_newlines(this_dir, git_hook_directory, 'post_commit.py')
    #
    return


def write_setup(project_directory):
    #
    abs_setup_file_name = join(project_directory, 'setup.py')
    setup_file_exists = isfile(abs_setup_file_name)
    if not setup_file_exists:
        create_new_setup_file(project_directory)
    else:
        modify_existing_setup_file(abs_setup_file_name)
    #
    return


def create_new_setup_file(project_directory):
    #
    project_name = basename(project_directory)
    abs_setup_file_name = join(project_directory, 'setup.py')
    #
    with open(join(this_dir, 'setup'), 'r') as setup_file:
        setup_template = setup_file.read()
        cp = config_parser()
        config_opts = cp.config_opts
        setup_template = setup_template.replace(
            'REPLACE_NAME', project_name
        ).replace(
            'REPLACE_AUTHOR', config_opts['author']
        ).replace(
            'REPLACE_EMAIL', config_opts['email']
        )
    #
    with open(abs_setup_file_name, 'w') as setup_py_file:
        setup_py_file.write(setup_template)
    #
    return


def modify_existing_setup_file(setup_file_name):
    #
    # Read base setup file
    with open(setup_file_name, 'r') as fr:
        base_setup_file_string = fr.read()
    #
    # Check to see if the version file has already been imported
    # from a previous track of this repository
    has_file_import = has_import_regex.search(base_setup_file_string)
    if has_file_import:
        setup_file_string = base_setup_file_string
    else:
        setup_file_string = base_setup_file_string.replace(r'setup(', setup_file_replacement_string)
    #
    # Check to see if the version is set to the version file import
    has_version_specified = version_regex.search(setup_file_string)
    if has_version_specified:
        final_setup_file_string = sub(version_pattern, 'version=version,', setup_file_string)
    else:
        final_setup_file_string = setup_file_string.replace(r'setup(', 'setup(version=version,')
    #
    # Write setup.py file
    with open(setup_file_name, 'w') as fw:
        fw.write(final_setup_file_string)
    #
    return
