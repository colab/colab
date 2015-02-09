
import os
import yaml

import yamlordereddictloader

from django.core.exceptions import ImproperlyConfigured


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

    if not os.path.exists(yaml_path):
        msg = "The yaml file {} does not exist".format(yaml_path)
        raise InaccessibleYAMLSettings(msg)

    yaml_settings = _load_yaml_file(yaml_path)

    # Try to read settings from settings.d
    if os.path.exists(settings_dir):
        for file_name in os.listdir(settings_dir):
            if file_name.endswith('.yaml') or file_name.endswith('yml'):
                file_path = os.path.join(settings_dir, file_name)
                yaml_settings_d = _load_yaml_file(file_path)
                yaml_settings.update(yaml_settings_d)

    return yaml_settings or {}

yaml_settings = load_yaml_settings()
