
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
    yaml_path = os.getenv('COLAB_SETTINGS', '/etc/colab/settings.yaml')

    if os.path.exists(yaml_path):
        global USING_YAML_SETTINGS
        USING_YAML_SETTINGS = True
        warnings.warn("YAML Settings file is deprecated. Use Py file instead.")
    else:
        return {}

    yaml_settings = _load_yaml_file(yaml_path)

    # Try to read settings from settings.d
    if os.path.exists(settings_dir):
        for file_name in os.listdir(settings_dir):
            if file_name.endswith('.yaml') or file_name.endswith('yml'):
                file_path = os.path.join(settings_dir, file_name)
                yaml_settings_d = _load_yaml_file(file_path)
                yaml_settings.update(yaml_settings_d)

    return yaml_settings or {}


class InaccessiblePySettings(ImproperlyConfigured):
    """Settings.py is Inaccessible.

    Check if the file exists and if you have read permissions."""


def _load_py_file(py_path):
    try:
        py_settings = importlib.import_module(py_path)

    except:
        msg = ('Could not open settings file {}. Please '
               'check if the file exists and if user '
               'has read rights.').format(py_path)
        raise InaccessiblePySettings(msg)

    return py_settings


def load_py_settings():
    settings_dir = '/etc/colab/settings.d'
    settings_module = 'settings'
    py_path = os.getenv('COLAB_SETTINGS',
                        "/etc/colab/{}.py".format(settings_module))

    global USING_YAML_SETTINGS
    if not os.path.exists(py_path) and not USING_YAML_SETTINGS:
        msg = "The py file {} does not exist".format(py_path)
        raise InaccessiblePySettings(msg)
    elif USING_YAML_SETTINGS:
        return {}

    sys.path.insert(0, '/etc/colab/')
    sys.path.insert(0, settings_dir)

    py_settings = _load_py_file(settings_module).__dict__

    # Try to read settings from settings.d
    if os.path.exists(settings_dir):
        for file_name in os.listdir(settings_dir):
            if file_name.endswith('.py'):
                file_module = file_name.split('.')[0]
                py_settings_d = _load_py_file(file_module).__dict__
                py_settings.update(py_settings_d)

    sys.path.remove('/etc/colab/')
    sys.path.remove(settings_dir)

    return py_settings or {}


def load_colab_apps():
    plugins_dir = '/etc/colab/plugins.d/'

    global USING_YAML_SETTINGS
    if USING_YAML_SETTINGS:
        return {}

    sys.path.insert(0, plugins_dir)

    COLAB_APPS = {}

    # Try to read settings from plugins.d
    if os.path.exists(plugins_dir):
        for file_name in os.listdir(plugins_dir):
            if file_name.endswith('.py'):
                file_module = file_name.split('.')[0]
                py_settings_d = _load_py_file(file_module)
                fields = ['urls', 'menu', 'upstream', 'middlewares',
                          'dependencies', 'context_processors']

                app_name = getattr(py_settings_d, 'name', None)
                if not app_name:
                    warnings.warn("Plugin missing name variable")
                    continue

                COLAB_APPS[app_name] = {}
                for key in fields:
                    value = getattr(py_settings_d, key, None)
                    if value:
                        COLAB_APPS[app_name][key] = value

    sys.path.remove(plugins_dir)

    return {'COLAB_APPS': COLAB_APPS}
