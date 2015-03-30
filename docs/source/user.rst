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

Declares the menu structure of the app, if it exists. It is a dictionary with
the folowing keys.

.. attribute:: title

    Declares the menu title. It's has a string value.
.. attribute:: links

    Declares the menu items and its links.
.. attribute:: auth_links

    Declares the menu items and its links when the user authenticated.
.. attribute:: dependecies

Example:

.. code-block:: python

   menu = {
      'title': _('Code'),
      'links': (
          (_('Public Projects'), 'public/projects'),
      ),
      'auth_links': (
          (_('Profile'), 'profile'),
          (_('New Project'), 'projects/new'),
          (_('Projects'), 'dashboard/projects'),
      ),
   }


Extra Template Folders
++++++++++++++++++++++

.. attribute:: COLAB_TEMPLATES

   :default: None

   Colab's extra template folders. Use it to add plugins template files.


Extra Static Folders
++++++++++++++++++++

.. attribute:: COLAB_STATIC

   :default: None

   Colab's extra static folders. Use it to add plugins static files.

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
