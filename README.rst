.. -*- coding: utf-8 -*-

.. highlight:: rest

.. _colab_software:

=================================
Colab, a Software for Communities
=================================


Installation (Development Environment)
==========================================

Here we'll cover how to setup a development environment using a Vagrant 
virtual machine.

Before getting started you should install the following softwares:

* Vagrant (tested with version 1.2.7)

* Virtualbox (version >= 4.0)

* fabric (tested with version 1.7.0)

* Git


Getting started with the Virtual Machine
------------------------------------------

First you will need to clone the repository:

.. code-block::

  git clone git@github.com:interlegis/colab.git


*NOTE:*

  Here we are assuming you have ssh permissions to clone the repo using ssh. If not
  fork it and clone your own fork (or use https instead of ssh).


Enter in the repository you've just cloned.
To start working all you need is to turn the virtual machine on with the command:

.. code-block::

  vagrant up


*NOTE:*

  BE PATIENT!
 
  This will take a while. The `vagrant up` will download a full vm (virtualbox)
  running a Ubuntu 12.04 64bits. After the vm is up and running the command
  will also configure it (using puppet) and that will also take a bit.
  

Running Colab
--------------

Now that you have a vm running we have two options to run Colab:

* Django development server (runserver)
 
* Gunicorn + supervisor + Nginx


Django development server (runserver)
++++++++++++++++++++++++++++++++++++++

This option is advised for developers working in new features for Colab.
The code used to run Colab will be the same code placed on your machine,
that means that if you change the code in your own computer the code on
the vm will also change.

Make sure you have a ``local_settings.py`` file placed in your repository. It
should be located in ``src/colab/``.

To get started you can copy the example file as follow:

.. code-block::

  cp src/colab/local_settings-dev.py src/colab/local_settings.py 


Now we are ready to run:

.. code-block::

  fab runserver
  

*Note*

  As this is the first time you run this command it will install all 
  requirements from ``requirements.txt`` into a virtualenv. To update 
  those requirements you should run ``fab runserver:update``. 


The ``fab runserver`` command will open the django builtin development
server on the port 7000 but due to vagrant magic you will be able to 
access it on ``http://localhost:8000/``.


Gunicorn + supervisor + Nginx
++++++++++++++++++++++++++++++

This option will run Colab in a way very similar to the production
environment. This should be used to test puppet manifests and also 
the configuration of each one of the services running.

First of all we need to clone the repo and configure your ``local_settings.py``.
That is done by calling the command:

.. code-block::

  fab install:path/to/your/local_settings.py


Now you need to deploy the code using the command:

.. code-block::

  fab deploy
  

For the next deploy you can just run ``fab deploy`` and in case your
``requirements.txt`` changes ``fab deploy:update``.

The deployed code will be accessible on ``http://localhost:8080``.
