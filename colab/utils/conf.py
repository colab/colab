
import os
import sys
import importlib
import warnings

from django.core.exceptions import ImproperlyConfigured


class InaccessibleSettings(ImproperlyConfigured):
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
        raise InaccessibleSettings(msg)

    except SyntaxError as excpt:
        msg = ('Syntax Error: {}'.format(excpt))
        raise InaccessibleSettings(msg)

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

    if not os.path.exists(py_path):
        msg = "The py file {} does not exist".format(py_path)
        raise InaccessibleSettings(msg)

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

    COLAB_APPS = {}

    # Try to read settings from plugins.d
    if os.path.exists(plugins_dir):
        for file_name in os.listdir(plugins_dir):
            if file_name.endswith('.py'):
                file_module = file_name.split('.')[0]
                py_settings_d = _load_py_file(file_module, plugins_dir)
                fields = ['verbose_name', 'upstream', 'urls',
                          'menu_urls', 'middlewares', 'dependencies',
                          'context_processors', 'private_token']

                app_name = py_settings_d.get('name')
                if not app_name:
                    warnings.warn("Plugin missing name variable")
                    continue

                COLAB_APPS[app_name] = {}
                COLAB_APPS[app_name]['menu_title'] = \
                    py_settings_d.get('menu_title')

                for key in fields:
                    value = py_settings_d.get(key)
                    if value:
                        COLAB_APPS[app_name][key] = value

    return {'COLAB_APPS': COLAB_APPS}
