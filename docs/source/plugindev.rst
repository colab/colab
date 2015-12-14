
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
represented on the html file. An example for this file can be seen bellow:

.. code-block:: guess

   {% load i18n tz highlight gravatar date_format %}

    <div class="row">
    <div class="col-md-2 center">
        <a href="{% url 'user_profile' username=result.username %}">
        {% block gravatar_img %}{% gravatar result.email 100 %}{% endblock gravatar_img %}
        </a>
    </div>
    <div class="col-md-10">
        <strong><a href="{% url 'user_profile' username=result.username %}">

            {% if query %}
                <h4>{% highlight result.name with query %}</h4></a>
            {% else %}
                <h4>{{ result.name }}</h4></a>
            {% endif %}

        </strong>
        <small><strong>{% trans "Since" %}: {% date_format result.date_joined %}</strong></small><br>
        <small>{% trans "Registered in" %}: <strong>{% trans "User" %}</strong></small><br>
    </div>
    </div>
    <div class="row">
    <hr>
    </div>

As can be seen in the above example, it also possible to highlight the elements being searched. This can be seen on
the following example:

.. code-block:: html

    {% if query %}
        <h4>{% highlight result.name with query %}</h4></a>
    {% else %}
        <h4>{{ result.name }}</h4></a>
    {% endif %}

It can be seen that if a query text was used on the search, it will highlight the element if it is present on the query, if not,
the element will be displayed without a highlight. Therefore, in order to highlight some fields, it is necessary
to first check if there is a query search. If there is, use the tag "highlight" before the field name. However, it
must be said that the highlight tag should be followed by a complement, such as "with query", as can be seen on the example
above. This complement is used to allow the highlight only if the attribute is actually present on the query used to perform a search.

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

   def has_special_char(username):
       for char in username:
           if char.isupper():
               return

       raise ValidationError('Username must have at least one upper case char')

   ## /etc/colab/plugins.d/myplugin.py

    username_validators = (
       'myplugin.username_validators.has_uppercase_char',
   )

