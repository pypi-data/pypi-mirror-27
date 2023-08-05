import ConfigParser
import os
import sys

from string import Template


def get_config_dict(**kwargs):

    if not kwargs.get('config_file'):
        config_file = '%s/%s' % (os.getcwd(), 'generator.cfg')
    else:
        file_path = os.path.dirname(os.path.realpath(__file__))
        config_file = '%s/%s' % (file_path, kwargs.get('config_file'))

    config = ConfigParser.RawConfigParser()

    if not os.path.isfile(config_file):
        print "Expected to find configuration file with the setup"
        create_flag = raw_input('Do you wanna create the config file? [Y/n]')

        if not create_flag or create_flag == "Y" or create_flag == "y": 
            with open(config_file, 'w') as f:
                cfg_tpl_path = os.path.dirname(os.path.realpath(__file__))
                cfg_tpl_path = '%s/%s' % (cfg_tpl_path.replace('utils', 'file_templates'), 'config.template')
                f.write(open(cfg_tpl_path).read())
                sys.exit()
        else: 
            sys.exit()

    config.readfp(open(config_file))

    if not kwargs.get('section_key') and not kwargs.get('config_file'):
        dirs_config_hash_map = config.items('dirs')
    else:
        dirs_config_hash_map = config.items(kwargs.get('section_key'))

    dirs_config_dict = {}

    for k, v in dirs_config_hash_map:
        dirs_config_dict[k] = v

    return dirs_config_dict


def get_extensions_dict():
    return get_config_dict(config_file='constants.cfg', section_key='extensions')


def get_files_dict():
    return get_config_dict(section_key='files')


def get_wildcards_dict():
    return get_config_dict(config_file='constants.cfg', section_key='wildcards')


def replace_content(file_path, substitution_dict):
    return Template(open(file_path).read()).substitute(substitution_dict)