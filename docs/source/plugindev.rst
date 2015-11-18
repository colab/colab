
.. _plugin-dev:

Plugin Developer Documentation
====================================

Getting Started
---------------

Signals
----------
Implement signals in plugins is optional! You may follow this steps only if you
want to communicate with another plugins.

In order to configure a plugin to able to listen and send signals using Colab
signals structure, some steps are required:

* In the apps.py file it is necessary to declare a list variable containing all
  the signals that the plugin will dispatch. It is suggested to name the
  variable "registered_signals", but that nomenclature not strictly necessary.
* It is also necessary to declare a variable containing the name of the plugin
  that will send the signal. It must be said that the name of the plugin cannot
  contain any special character, such as dot or comma. It is suggested to name
  the variable "short_name", but that nomenclature is not strictly
  necessary.
* In order to actually register the signals, it is necessary to implement the
  method register_signal, which require the name of the plugin that is
  registering the signals and a list of signals to be registered as parameters.
  You must not call this method nowhere.
* In order to listen for a given signal, it is required to create a handling
  method. This method should be located at a file named tasks.py in the same
  directory as the plugins files. It also must be said that this method need to
  receive at least a \*\*kwargs parameter. An example of a handling method can
  be seen below:

.. code-block:: python
   from colab.celery import app

   @app.task(bind=True)
   def handling_method(self, **kwargs):
       # DO SOMETHING

* With signals registered and handling method defined you must connect them.
  To do it you must call connect_signal passing signal name, sender and handling
  method as arguments. These should be implemented on plugin's apps.py. It must
  be said that the plugin app class must extend ColabPluginAppConfig. An
  example of this configuration can be seen below:


.. code-block:: python
   from colab.plugins.utils.apps import ColabPluginAppConfig
   from colab.signals.signals import register_signal, connect_signal
   from colab.plugins.PLUGIN.tasks import HANDLING_METHOD

   class PluginApps(ColabPluginAppConfig):
        short_name = PLUGIN_NAME
        signals_list = [SIGNAL1, SIGNAL2]

        def registered_signal(self):
            register_signal(self.short_name, self.signals_list)

        def connect_signal(self):
            connect_signal(self.signals_list[0], self.short_name,
              HANDLING_METHOD)
            connect_signal(self.signals_list[1], self.short_name,
              HANDLING_METHOD)


* To send a broadcast signal you must call send method anywhere passing signal
  name and sender as arguments. If necessary you can pass another parameters in
  \*\*kwargs. As you can see below:

.. code-block:: python
   from colab.signals.signals import send

   send(signal_name, sender)

* If you want to run celery manually to make some tests, you should execute:

.. code-block:: shell
   colab-admin celeryC worker --loglevel=debug
