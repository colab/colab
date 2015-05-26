User Documentation
==================

Getting Started
---------------

Dependencies
++++++++++++
.. TODO

Install
+++++++
.. TODO

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

urls
++++

.. attribute:: include

    Declares the include urls.
.. attribute:: prefix

    Declares the prefix for the url.
.. attribute:: namespace

    Declares the namespace for the url.

menu
++++

These variables defines the menu title and links of the plugin.

.. attribute:: menu_title

    Declares the menu title.
.. attribute:: menu_links

    Declares the menu items and its links.
    This should be a tuple object with several colab_url elements.
    The colab_url_factory creates a factory for your links along with your
    namespace.
    The auth parameter indicates wether the link should only be displayed when
    the user is logged in.

Example:

.. code-block:: python

    from colab.plugins.utils.menu import colab_url_factory

    url = colab_url_factory('plugin_app_name')

    menu_urls = (
       url(display=_('Profile'), viewname='profile', kwargs={'path': '/profile/'}, auth=True),
       url(display=_('Profile Two'), viewname='profile2', kwargs={'path': '/profile/2'}, auth=True),
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

Blog Planet
+++++++++++
.. TODO

Paste
+++++
.. TODO

XMPP
++++
.. TODO

SVN
+++
.. TODO

Social Networks
+++++++++++++++
.. attribute:: SOCIAL_NETWORK_ENABLED

   :default: False

   When this variable is True, the social networks fields, like Facebook and
   Twitter, are added in user profile. By default, this fields are disabled.

Auth
++++
.. attribute:: BROWSERID_ENABLED

   :default: False

   When this variable is True, Colab use BrowserID authentication. By default,
   django authentication system is used.

.. attribute:: BROWSERID_AUDIENCES

   :default: No default

   List of audiences that your site accepts. An audience is the protocol,
   domain name, and (optionally) port that users access your site from. This
   list is used to determine the audience a user is part of (how they are
   accessing your site), which is used during verification to ensure that the
   assertion given to you by the user was intended for your site.

   Without this, other sites that the user has authenticated with via Persona
   could use their assertions to impersonate the user on your site.

   Note that this does not have to be a publicly accessible URL, so local URLs
   like ``http://localhost:8000`` or ``http://127.0.0.1`` are acceptable as
   long as they match what you are using to access your site.

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
