User Documentation
==================

Getting Started
---------------

Install Requirements with Vagrant
+++++++++++++++++++++++++++++++++

Need VirtualBox and Vagrant installed

Run the following command to create and up the colab virtual machine

.. code-block:: shell

    $ vagrant up

Run the following command to access colab virtual machine

.. code-block:: shell

      $ vagrant ssh

Install Requirements without Vagrant
++++++++++++++++++++++++++++++++++++

Install virtualenvwrapper

Use this link to configure the virtualenvwreapper: https://virtualenvwrapper.readthedocs.org

Run the following command

.. code-block:: shell

    $ mkvirtualenv colab

Install Development
+++++++++++++++++++

On the colab folder use the following commands, or in the colab vagrant ("$ vagrant ssh")

.. code-block:: shell

    $ workon colab
    $ pip install -e . #(dont need this command if use vagrant)
    $ colab-admin migrate #(dont need this command if use vagrant)
    $ colab-admin runserver 0.0.0.0:8000


Colab settings
+++++++++++++++++

View the following file:

.. code-block:: shell

    $ cat /etc/colab/settings.py

The file /etc/colab/settings.py have the configurations of colab, this configurations overrides the django settings.py

Colab can generate its own default settings file for development environment with

.. code-block:: shell

   $ colab-admin initconfig > /etc/colab/settings.py

Colab development settings - Log Level
++++++++++++++++++

If you used the default settings file from initconfig. You can especify the environment variable **COLAB_LOGLEVEL** to set which log level you want to
show on the console.

You can also set **COLAB_DEBUG** that is an alias to *COLAB_LOGLEVEL=DEBUG*

The following log levels exist:

* **DEBUG**: Show everything possible.
* **INFO**: Show info, and errors.
* **ERROR**: Default behavior, show errors, warnings and critical messages.

Example of running runserver showing **INFO** logs:

.. code-block:: shell

   $ COLAB_LOGLEVEL=INFO colab-admin runserver 0.0.0.0:8000

Widgets
-------

A widget is a piece of HTML that will be inserted in a specific area in a page to render some view.

To configure the widgets you have to edit, or create, the file ``/etc/colab/widgets_settings.py``. Or you can create a py file inside the folder ``/etc/colab/widgets.d``.

Example:

.. code-block:: python

   # Widget Manager handles all widgets and must be imported to register them
   from colab.widgets.widget_manager import WidgetManager

   # Specific code for Gitlab's Widget
   from colab_gitlab.widgets import GitlabProfileWidget

   WidgetManager.register_widget('profile', GitlabProfileWidget())


In this example the Gitlab's widget is added in a new tab inside the user profile.

Widgets Areas
+++++++++++++

.. attribute:: List

    The list widget area can be found at the user profile. It provides general information like latest news and collaboration.

.. attribute:: Button

    The button widget area can be found at the user profile. It provides aditional buttons to profile.

.. attribute:: Group

    The group widget area can be found at the user profile. It provides aditional information to profile.

.. attribute:: Dashboard

    The dashboard widget area can be found at ``/dashboard``. It provides general information like latest news and collaboration.

.. attribute:: Charts

    The charts widget area can be found at the user profile page. It provides an area for charts displays.

Core Widgets
++++++++++++

.. attribute:: Most Relevant Threads

    Shows the list of most relevant threads.

    .. code-block:: python

       # Widget Manager handles all widgets and must be imported to register them
       from colab.widgets.widget_manager import WidgetManager

       # Specific code for Gitlab's Widget
       from colab_gitlab.widgets import GitlabProfileWidget

       WidgetManager.register_widget('profile', GitlabProfileWidget())

.. attribute:: Latest Threads

    Shows the list of latest threads, those threads are get from the public mailling lists.

.. attribute:: Groups

    Shows the groups that user is subscribed.

    **Suggested area:** group

.. attribute:: Group Membership

    Adds a button to subscribed in a group.

    **Suggested area:** button

.. attribute:: Latest Posted

    Shows the list of latest post, those post are get from the public mailling lists from the user.

    **Suggested area:** list

.. attribute:: Your Latest Contributions

    Shows the list of latest contributions for the user.

    **Suggested area:** list

.. attribute:: Latest Collaborations

    Shows the list of latest collaborations, in example, articles and blog post done recently.

    **Suggested area:** dashboard

.. attribute:: Collaboration Graph

    Displays a pie chart of all collaborations that are indexed.

    **Suggested area:** dashboard

.. attribute:: Collaboration Chart

    Displays a pie chart of all collaborations created by user that are indexed.

    **Suggested area:** charts

.. attribute:: Participation Chart

    Displays a pie chart of all participations from mail list.

    **Suggested area:** charts


Add a new plugin
----------------
- Atention: replace the brackets, [], for the content presented in the brackets

- Make sure the application has the following requirements

  - Support for remote user authentication

  - A relative url root

  - A relative static url root, for change url's of css and javascript

- Create the plugin configuration for the application

  - on folder: /etc/colab/plugins.d/

  - create file: [plugin_name].py

- Atention: Any URL used in the plugins' settings should not be preceded by "/"

Use this template for the plugin configuration file

.. code-block:: python

    from colab.plugins.utils.menu import colab_url_factory
    from django.utils.translation import ugettext_lazy as _

    name = 'colab.plugins.[plugin_name]'

    upstream = 'http://[host_of_application]/[relative_url_root]/'

    # The private_token is optional
    # It is used to access the application data being coupled to colab
    # It is recommended to use the provate_token an admin of the application
    private_token = '[plugin_private_token_for_data_import]'

    urls = {
        'include': '[plugin_module_path].urls',
        'prefix': '[application_prefix]/', # Exemple: http://site.com/[application_prefix]/
    }

    menu_title = '[menu_title_of_html]'

    url = colab_url_factory('[plugin_name]')

    menu_urls = {
        url(display=_('[name_of_link_page]'), viewname='[name_of_view_in_the_application]', kwargs={'path': '[page_appication_path]/' }, auth=True),

        # You can have more than one url
        url(display=_('[name_of_link_page]'), viewname='[another_name_of_view_in_the_application]', kwargs={'path': '[another_page_appication_path]/' }, auth=True),
    }




Plugins
-------
.. attribute:: name

Declares the absolute name of the plugin app as a python import path. Example:
directory.something.someplugin

.. attribute:: verbose_name

Delclare the description name of the plugin.

.. attribute:: upstream

Declares the upstream server url of the proxy. Only declare if the plugin is a
proxy.

.. attribute:: middlewares

Declares the middlewares of the plugin in a list format.

.. attribute:: context_processors

Declares the context processors of the plugin in a list format too.

.. attribute:: dependency

Declares the additional installed apps that this plugin depends on.
This doesn't automatically install the python dependecies, only add to django
apps.

.. attribute:: password_validators

A lista of functions to validade password in the moment it's set.
This allows plugins to define their own password validators. For
example if the proxied app requires the password to have at least
one upper case character it should provide a password validator
for that.


urls
++++

.. attribute:: include

    Declares the include urls.
.. attribute:: prefix

    Declares the prefix for the url.

    - Atention: Any URL used in the plugins' settings should not be preceded by "/"

menu
++++

These variables defines the menu title and links of the plugin.

.. attribute:: menu_title

    Declares the menu title.
.. attribute:: menu_urls

    Declares the menu items and its links.
    This should be a tuple object with several colab_url elements.
    The colab_url_factory creates a factory for your links along with your
    namespace.
    The auth parameter indicates wether the link should only be displayed when
    the user is logged in.
    The ``kwargs`` parameter receives a dict, where the key ``path`` should be
    a path URL to the page. Remember that this path is a URL, therefore it
    should never be preceded by "/".

Example:

.. code-block:: python

    from colab.plugins.utils.menu import colab_url_factory

    url = colab_url_factory('plugin_app_name')

    menu_urls = (
       url(display=_('Profile'), viewname='profile', kwargs={'path': 'profile/'}, auth=True),
       url(display=_('Profile Two'), viewname='profile2', kwargs={'path': 'profile/2'}, auth=True),
    )

Extra Template Folders
++++++++++++++++++++++

.. attribute:: COLAB_TEMPLATES

   :default: () (Empty tuple)

   Colab's extra template folders. Use it to add plugins template files, and
   remember to use the app hierarchy, e.g if your app name is example, then
   you should put your templates inside ``COLAB_TEMPLATES/example``.
   You can also use it to overwrite the default templates, e.g. if you want
   to overwrite the default footer, you simply need to add a file named
   ``footer.html`` to the folder where ``COLAB_TEMPLATES`` points to.

Extra Static Folders
++++++++++++++++++++

.. attribute:: COLAB_STATIC

   :default: [] (Empty list)

   Colab's extra static folders. Use it to add plugins static files. It's used
   the same way COLAB_TEMPLATES is. Use it to overwrite or add your own static
   files, such as CSS/JS files and/or images.


Settings
--------

Paste
+++++
.. TODO

Social Networks
+++++++++++++++
.. attribute:: SOCIAL_NETWORK_ENABLED

   :default: False

   When this variable is True, the social networks fields, like Facebook and
   Twitter, are added in user profile. By default, this fields are disabled.


Customization
-------------
Home Page
+++++++++
.. TODO

Menu
++++
.. TODO

Templates
+++++++++
.. TODO

Verify Inactive User
++++++++

.. attribute:: ACCOUNT_VERIFICATION_TIME

   :default: timedelta(hours=48)

   This variable will be used to remove inactive user.
   By default, this time is 48 hours.
