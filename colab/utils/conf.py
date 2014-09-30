
import os
import yaml

from django.core.exceptions import ImproperlyConfigured


class InaccessibleYAMLSettings(ImproperlyConfigured):
    """Settings YAML is Inaccessible.

    Check if the file exists and if you have read permissions."""


def load_yaml_settings():
    yaml_path = os.getenv('COLAB_SETTINGS', '/etc/colab.yaml')

    if not os.path.exists(yaml_path):
        msg = "The yaml file {} does not exist".format(yaml_path)
        raise InaccessibleYAMLSettings(msg)

    try:
        with open(yaml_path) as yaml_file:
            yaml_settings = yaml.load(yaml_file.read())
    except IOError:
        msg = ('Could not open settings file {}. Please '
               'check if the file exists and if user '
               'has read rights.').format(yaml_path)
        raise InaccessibleYAMLSettings(msg)

    return yaml_settings

yaml_settings = load_yaml_settings()
