
.. _plugin-dev:

Plugin Developer Documentation
====================================

Getting Started
---------------

To start a new plugin, run the command:

.. code-block:: bash

   $ colab-admin startplugin plugin_name [directory]

Where ``plugin_name`` is the name of your new plugin. And ``directory``, which
is optional, specifies the directory where the structure of your plugin will be
created.

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
* Finally, the variable namespace should also be defined. This variable is the
  url namespace for django reverse.
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
        namespace = PLUGIN_NAMESPACE

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

Search
----------

In order to make some plugin model's searchable, it is necessary to create
some files. First of all, it is necessary to create a directory named "search"
inside the templates directory, that should be found on the plugin root
directory.

Once the search folder exist, it is necessary to create a html file that will
describe how a model item will be displayed on the colab search page. This file
name must follow the pattern:

MODELNAME_search_preview.html

Where the MODELNAME should be the name of the model object that will be
represented on the html file. In this template, you can set the following variables:

* ``modified``: value in django datetime format.
* ``modified_time``: if setted as True, it shows ``modified`` date and time.
* ``author``: HTML code with a link of responsible for the result profile.
* ``url``: link for the result location.
* ``title``: title of the result.
* ``description``: description of the result.
* ``registered_in``: category of the result, as string.

To set variables, you have to load the set_var templatetag (``{% load set_var %}``) in your template, then you can set the variables using this syntax:

``{% set 'variable_name' variable_value %}``

If you don't want a variable to be showed, you just shouldn't set it.

These variables will be used in the below code:

.. code-block:: html

    {% load i18n tz highlight %}
    {% block content %}
      <div class="row">
        <div class="col-md-12">
          <small>{{ modified|date:"d F Y"|default_if_none:"" }}
            {% if modified_time %}
              {% trans "at" %} {{result.modified|date:"h:m" }}
            {% endif %}
            {{author|safe|default_if_none:""}}
          </small><br>
          <h4><a href="{{url}}">
            {% if title %}
              {% highlight title with query %}
            {% endif %}
          </a></h4>
          <p>
            {% if description != "None" %}
              <a href="{{url}}">{% highlight description with query %}</a>
            {% endif %}
          </p>
          {% if registered_in %}
            <small class="colab-result-register">{% trans "Registred in" %}:
              <strong>{% trans registered_in %}</strong>
            </small>
          {% endif %}
        </div>
        <hr>
      </div>
    {% endblock content %}

As you can see above, it also possible to highlight the elements being searched.

To illustrate how to use this template base, see the following code:

.. code-block:: html

  {% extends "search-base.html" %}
  {% load set_var %}
  {% block content %}
    {% set 'title' result.title %}
    {% set 'modified' result.modified %}
    {% set 'url' result.url %}
    {% set 'registered_in' "Code" %}
    {% set 'description' result.description|default_if_none:" "|truncatechars:"140" %}

    {{ block.super }}
  {% endblock content %}

And the follow HTML will be generated:

.. code-block:: html

  <div class="row">
    <div class="col-md-12">
      <small>24 October 2014
      </small><br>
      <h4><a href="/gitlab/softwarepublico/colab/merge_requests/1">
          Settings fix
      </a></h4>
      <p>
          <a href="/gitlab/softwarepublico/colab/merge_requests/1"> </a>
      </p>
        <small class="colab-result-register">Registred in:
          <strong>Code</strong>
        </small>
    </div>
    <hr>
  </div>


If your search preview doesn't match the base template, you just don't have to extend it and make your own HTML.


Also a another file that must be created is the search_index.py one. This file
must be placed at the plugin root directory. This file dictates how haystack
will index the plugins models. If there is any doubt about how to create this
file, it's possible to check the official haystack documentation that can be
seen on the bellow link.

`Guide to create a SearchIndexesFiles`_

.. _`Guide to create a SearchIndexesFiles`: http://django-haystack.readthedocs.org/en/v2.4.0/tutorial.html#creating-searchindexes

It can also be seen in the guide above that an indexes directory should be
created. This directory should be placed inside the search directory originally
created in this tutorial. Inside this directory, create a txt file for each
model that can be queried. Each of this files must contain the model fields that
will be search if no filter is applied. If there is any doubts to create these
files, please check the `Guide to create a SearchIndexesFiles`_.

Storing TimeStamp
---------------
TimeStamp is a parameter to control the last time a model was updated, you should use it
when you want the data updated after a given time. To do that the colab's model (colab.plugins.models) have a
TimeStampPlugin class, used to store all last updates from timestamp from all plugins.

Class Methods:
   update_timestamp(cls,class_name): allow store a current datetime.

   get_last_updated_timestamp(cls,class_name): allow get a datetime with last timestamp stored from class_name.

Example Usage:

.. code-block:: python
   from colab.plugins.models import TimeStampPlugin

   class TestPlugin():

       def update_timestamp(self):
          TimeStampPlugin.update_timestamp('TestPlugin')

       def get_last_updated_timestamp(self):
          return TimeStampPlugin.get_last_updated_timestamp('TestPlugin')


Password Validation
-------------------

Allows the plugin to define rules to set the password. The validators
are functions which receive the password as only argument and if it
doesn't match the desired rules raises a `ValidationError`. The message
sent in the validation error will be displayed to user in the HTML form.

Example:

.. code-block:: python

   ## myplugin/password_validators.py

   def has_uppercase_char(password):
       for char in password:
           if char.isupper():
               return

       raise ValidationError('Password must have at least one upper case char')

   ## /etc/colab/plugins.d/myplugin.py

   password_validators = (
       'myplugin.password_validators.has_uppercase_char',
   )

Username Validation
-------------------

Allows the plugin to define rules to set the username. The validators
are the same as the password validators ones. Therefore, they follow the same
structure.

Example:

.. code-block:: python

   ## myplugin/username_validators.py

   def has_uppercase_char(username):
       for char in username:
           if char.isupper():
               return

       raise ValidationError('Username must have at least one upper case char')

   ## /etc/colab/plugins.d/myplugin.py

    username_validators = (
       'myplugin.username_validators.has_uppercase_char',
   )

Blacklist
-------------------

If you don't want a page to be accessed, you should add in your configuration file
(/etc/colab/plugins.d) an array of regex strings named 'blacklist' that
stands for the urls. The pages will then return a 403 error (forbidden).


Ex:

.. code-block:: python

    blacklist = [r'^dashboard$']

It also must be said that the full url will that will be blocked is a
combination of the plugin prefix and one of the elements of the blacklist array.
For example, given a plugin with this configuration:


.. code-block:: python

    urls = {
        'include': 'colab_plugin.urls',
        'prefix':  '^plugin/',
        }

    blacklist = [r'^feature$']

The actual url that will be blocked will them be: plugin/feature.


Change Header
-----------------

If you want to change the header on your plugin pages, you should add in your
configuration file (/etc/colab/plugins.d/) a boolean variable 'change_header',
where True uses the slim header and False uses the default header. The default value
of 'change_header' variable is False.

.. code-block:: python

    urls = {
        'include': 'colab_plugin.urls',
        'prefix':  '^plugin/',
        }

    change_header = True
