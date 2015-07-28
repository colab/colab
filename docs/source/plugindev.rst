
.. _plugin-dev: 

Plugin Developer Documentation
====================================

Getting Started
---------------

Signals
----------

In order to configure a plugin to able to listen and send signals using Colab
signals structure, some steps are required:

* Every plugin that needs to handle signals in colab need to use celery in order
  to run taks asynchronously. This is due the fact that every time a handling
  method for a signal is executed, it will be executed as a asynchronously
  celery tasks, in order to not block other colab tasks. To use celery in the
  plugin,  file named celery.py needs to be created on the root directory of the
  plugin. An example file can be seen below:

.. code-block:: python

    m __future__ import absolute_import

    import os

    from celery import Celery

    # set the default Django settings module for the 'celery' program.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'colab.settings')

    from django.conf import settings

    app = Celery('colab')

    app.config_from_object('django.conf:settings')
    app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

    app.conf.update(
        CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend',
    )
    app.conf.update(
        CELERY_RESULT_BACKEND='djcelery.backends.cache:CacheBackend',
    )

* The plugin should import the method from colab.signals.tasks in order for the
  plugin to use the necessary method to handle signals
* In the apps.py file it is necessary to declare a list variable containing all the
  signals that the plugin will dispatch. It is suggested to name the variable
  "registered_signals", but that nomenclature not strictly necessary.
* It is also necessary to declare a variable containing the name of the plugin
  that will send the signal. It must be said that the name of the plugin cannot
  contain any special character, such as dot or comma. It is suggested to name
  the variable "short_name", but that nomenclature is not strictly
  necessary.
* In order to actually register the signals, it is necessary to call the method
  register_signal, which require the name of the plugin that is registering the
  signals and a list of signals to be registered as parameters. This method
  should be called on the app method named __init__. Since the plugin class is a
  subclass of AppConfig, the constructor of the parent must be calles as weel.

.. code-block:: ṕython
   def __init__(self, app_name, app_module):
       super(ProxyGitlabAppConfig, self).__init__(app_name, app_module)
       register_signal(self.short_name, self.signals_list)

* In order to listen for a given signal, it is required to create a handling
  method. This method should be located at a file named tasks.py in the same
  directory as the plugins files. It also must be said that this method need to
  receive at least a \*\*kwargs parameter. An example of a handling method can
  be seen below:

.. code-block:: python
   # import app from celery.py

   @app.task(bind=True)
   def handling_method(self, **kwargs):
       # DO SOMETHING

* With signals registered and handling method defined you must connect them.
  To do it you must call connect_signal passing signal name, sender and handling
  method as arguments. This calling must be into ready function in apps.py, as
  you can see below:

.. code-block:: python
   def ready(self):
     connect_signal(self.signal_name, self.sender, handling_method)

* To send a broadcast signal you must call send method anywhere passing signal name
  and sender as arguments. If necessary you can pass another parameters in
  \*\*kwargs. As you can see below:

.. code-block:: python
   send(signal_name, sender)

* If you want to run celery manually to make some tests, you should execute:

.. code-block:: shell
   celery -A colab worker --loglevel=debug
