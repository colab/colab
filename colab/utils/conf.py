
import os
import sys
import logging
import importlib

from django.core.exceptions import ImproperlyConfigured

logger = logging.getLogger('colab.init')
if os.environ.get('COLAB_DEBUG'):
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.DEBUG)


class InaccessibleSettings(ImproperlyConfigured):
    """Settings.py is Inaccessible.

    Check if the file exists and if you have read permissions."""


class DatabaseUndefined(ImproperlyConfigured):
    """Default database is not set.

    When DEBUG is set to True a local sqlite database can be used for
    developement porposes but otherwise the `default` database must
    be set."""


def _load_py_file(py_path, path):

    sys.path.insert(0, path)
    try:
        py_settings = importlib.import_module(py_path)

    except ImportError:
        msg = ('Could not open settings file {}. Please '
               'check if the file exists and if user '
               'has read rights.').format(py_path)
        raise InaccessibleSettings(msg)

    except SyntaxError as excpt:
        msg = ('Syntax Error: {}'.format(excpt))
        raise InaccessibleSettings(msg)

    finally:
        # We did not catch the ValueError on purpose
        #   If the imported module change the path
        #   we want to raise ValueError
        sys.path.remove(path)

    py_setting = {var: getattr(py_settings, var) for var in dir(py_settings)
                  if not var.startswith('_')}

    return py_setting


def load_py_settings(settings_dir='/etc/colab/settings.d'):
    settings_file = os.getenv('COLAB_SETTINGS', '/etc/colab/settings.py')
    settings_module = settings_file.split('.')[-2].split('/')[-1]
    py_path = "/".join(settings_file.split('/')[:-1])

    logger.info('Settings file: %s', settings_file)

    if not os.path.exists(py_path):
        msg = "The py file {} does not exist".format(py_path)
        raise InaccessibleSettings(msg)

    py_settings = _load_py_file(settings_module, py_path)

    logger.info('Settings directory: %s', settings_dir)

    if not os.path.exists(settings_dir):
        return py_settings

    for file_name in os.listdir(settings_dir):
        if not file_name.endswith('.py'):
            continue

        file_module = file_name.split('.')[0]
        py_settings_d = _load_py_file(file_module, settings_dir)
        py_settings.update(py_settings_d)
        logger.info('Loaded %s/%s', settings_dir, file_name)

    return py_settings


def load_colab_apps():
    plugins_dir = os.getenv('COLAB_PLUGINS', '/etc/colab/plugins.d/')
    logger.info('Plugin settings directory: %s', plugins_dir)

    COLAB_APPS = {}

    # Try to read settings from plugins.d
    if not os.path.exists(plugins_dir):
        return {'COLAB_APPS': COLAB_APPS}

    for file_name in os.listdir(plugins_dir):
        app_name = ""
        file_module = file_name.split('.')[0]

        logger.info('Loading plugin settings: %s%s', plugins_dir, file_name)

        # FIXME Drop plugins in plugins.d directory
        if os.path.isdir(os.path.join(plugins_dir, file_name)):
            py_settings_d = _load_py_file(file_module, plugins_dir)
            app_name = file_name

        elif file_name.endswith('.py'):
            py_settings_d = _load_py_file(file_module, plugins_dir)
            app_name = py_settings_d.get('name', '')

        else:
            logger.info("Not a plugin config: %s", file_name)
            continue

        if not app_name:
            logger.warning("Plugin missing name variable (%s)", file_name)
            continue

        try:
            importlib.import_module(app_name)
        except ImportError:
            logger.warning("Cannot import plugin %s (%s)", app_name, file_name)
            continue

        app_label = app_name.split('.')[-1]
        COLAB_APPS[app_label] = {}
        COLAB_APPS[app_label] = py_settings_d

    return {'COLAB_APPS': COLAB_APPS}


def load_widgets_settings():
    settings_file = os.getenv('COLAB_WIDGETS_SETTINGS',
                              '/etc/colab/widgets_settings.py')
    settings_module = settings_file.split('.')[-2].split('/')[-1]
    py_path = "/".join(settings_file.split('/')[:-1])
    logger.info('Widgets Settings file: %s', settings_file)

    if not os.path.exists(py_path):
        return

    original_path = sys.path
    sys.path.append(py_path)

    if os.path.exists(settings_file):
        importlib.import_module(settings_module)

    # Read settings from widgets.d
    settings_dir = os.getenv('COLAB_WIDGETS', '/etc/colab/widgets.d')
    logger.info('Widgets Settings directory: %s', settings_dir)
    sys.path = original_path

    if not os.path.exists(settings_dir):
        return

    for file_name in os.listdir(settings_dir):
        if not file_name.endswith('.py'):
            continue

        original_path = sys.path
        sys.path.append(settings_dir)

        file_module = file_name.split('.')[0]
        importlib.import_module(file_module)
        logger.info('Loaded %s/%s', settings_dir, file_name)

        sys.path = original_path


def validate_database(database_dict, default_db, debug):
    db_name = database_dict.get('default', {}).get('NAME')
    if not debug and db_name == default_db:
        msg = ('Since DEBUG is set to False DATABASE must be set on '
               'Colab settings')
        raise DatabaseUndefined(msg)
