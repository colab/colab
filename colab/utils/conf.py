
import os
import sys

import warnings

import yaml

import yamlordereddictloader

from django.core.exceptions import ImproperlyConfigured

import importlib


USING_YAML_SETTINGS = False


class InaccessibleYAMLSettings(ImproperlyConfigured):
    """Settings YAML is Inaccessible.

    Check if the file exists and if you have read permissions."""


def _load_yaml_file(yaml_path):
    try:
        with open(yaml_path) as yaml_file:
            yaml_settings = yaml.load(yaml_file.read(),
                                      yamlordereddictloader.Loader)
    except IOError:
        msg = ('Could not open settings file {}. Please '
               'check if the file exists and if user '
               'has read rights.').format(yaml_path)
        raise InaccessibleYAMLSettings(msg)

    return yaml_settings


def load_yaml_settings():
    settings_dir = '/etc/colab/settings.d'
    yaml_path = os.getenv('COLAB_YAML_SETTINGS', '/etc/colab/settings.yaml')

    if os.path.exists(yaml_path):
        global USING_YAML_SETTINGS
        USING_YAML_SETTINGS = True
        warnings.warn("YAML Settings file is deprecated. Use Py file instead.")
    else:
        return {}

    yaml_settings = _load_yaml_file(yaml_path)

    parse_yml_menus(yaml_settings)

    # Try to read settings from settings.d
    if os.path.exists(settings_dir):
        for file_name in os.listdir(settings_dir):
            if file_name.endswith('.yaml') or file_name.endswith('yml'):
                file_path = os.path.join(settings_dir, file_name)
                yaml_settings_d = _load_yaml_file(file_path)

                parse_yml_menus(yaml_settings_d)

                yaml_settings.update(yaml_settings_d)

    return yaml_settings or {}


class InaccessiblePySettings(ImproperlyConfigured):
    """Settings.py is Inaccessible.

    Check if the file exists and if you have read permissions."""


def _load_py_file(py_path, path):
    original_path = sys.path

    sys.path = [path]
    try:
        py_settings = importlib.import_module(py_path)

    except IOError:
        msg = ('Could not open settings file {}. Please '
               'check if the file exists and if user '
               'has read rights.').format(py_path)
        raise InaccessiblePySettings(msg)

    except SyntaxError as excpt:
        msg = ('Syntax Error: {}'.format(excpt))
        raise InaccessiblePySettings(msg)

    finally:
        sys.path = original_path

    py_setting = {var: getattr(py_settings, var) for var in dir(py_settings)
                  if not var.startswith('__')}

    return py_setting


def load_py_settings():
    settings_dir = '/etc/colab/settings.d'
    settings_file = os.getenv('COLAB_SETTINGS', '/etc/colab/settings.py')
    settings_module = settings_file.split('.')[-2].split('/')[-1]
    py_path = "/".join(settings_file.split('/')[:-1])

    global USING_YAML_SETTINGS
    if not os.path.exists(py_path) and not USING_YAML_SETTINGS:
        msg = "The py file {} does not exist".format(py_path)
        raise InaccessiblePySettings(msg)
    elif USING_YAML_SETTINGS:
        return {}

    py_settings = _load_py_file(settings_module, py_path)

    # Try to read settings from settings.d

    if os.path.exists(settings_dir):
        return py_settings
        for file_name in os.listdir(settings_dir):
            if file_name.endswith('.py'):
                file_module = file_name.split('.')[0]
                py_settings_d = _load_py_file(file_module, settings_dir)
                py_settings.update(py_settings_d)

    return py_settings


def load_colab_apps():
    plugins_dir = os.getenv('COLAB_PLUGINS', '/etc/colab/plugins.d/')

    global USING_YAML_SETTINGS
    if USING_YAML_SETTINGS:
        return {}

    COLAB_APPS = {}

    # Try to read settings from plugins.d
    if os.path.exists(plugins_dir):
        for file_name in os.listdir(plugins_dir):
            if file_name.endswith('.py'):
                file_module = file_name.split('.')[0]
                py_settings_d = _load_py_file(file_module, plugins_dir)
                fields = ['urls', 'menu', 'upstream', 'middlewares',
                          'dependencies', 'context_processors']

                app_name = py_settings_d.get('name')
                if not app_name:
                    warnings.warn("Plugin missing name variable")
                    continue

                COLAB_APPS[app_name] = {}
                for key in fields:
                    value = py_settings_d.get(key)
                    if value:
                        COLAB_APPS[app_name][key] = value

    return {'COLAB_APPS': COLAB_APPS}


def parse_yml_menus(yaml_settings):
    if 'COLAB_APPS' in yaml_settings:
        for key, plugin in yaml_settings['COLAB_APPS'].items():
            if 'menu' in plugin:
                parse_yml_tuples(yaml_settings['COLAB_APPS'][key]['menu'])


def parse_yml_tuples(menu):
    dict_links = menu['links']
    dict_auth_links = menu['auth_links']
    menu['links'] = tuple()
    menu['auth_links'] = tuple()

    for key, value in dict_links.items():
        menu['links'] += ((key, value),)

    for key, value in dict_auth_links.items():
        menu['auth_links'] += ((key, value),)
