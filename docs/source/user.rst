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
.. attribute:: COLAB_APPS

   :default: None

   Describes the activated plugins and its configurations. It's necessary to describe
   for each app its name as the variable. The apps described here can be devided into
   two categories, that beeing, colab proxy apps and third-party apps.
   The upstream variable is only needed to colab proxy apps.

.. attribute:: upstream

Declares the upstream server url of the proxy.

menu
++++++++++++

.. attribute:: title

    Declares the menu title.
.. attribute:: links

    Declares the menu items and its links.
.. attribute:: auth_links

    Declares the menu items and its links when the user authenticated.
.. attribute:: dependecies

Declares a list of the plugin dependecies.

urls
++++++++++++

.. attribute:: include

    Declares the include urls.
.. attribute:: prefix

    Declares the prefix for the url.
.. attribute:: namespace

    Declares the namespace for the url.

context_processors
++++++++++++

    Declares the plugin context processors.

middlewares
++++++++++++
    Declares the plugin middlewares.

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
++++
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
