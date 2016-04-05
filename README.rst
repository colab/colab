.. -*- coding: utf-8 -*-

.. highlight:: rest

.. _colab_software:

=================================
Colab, a Software for Communities
=================================

.. image:: https://travis-ci.org/colab/colab.svg?branch=master
    :target: https://travis-ci.org/colab/colab

.. image:: https://coveralls.io/repos/colab/colab/badge.png?branch=master
          :target: https://coveralls.io/r/colab/colab?branch=master


What is Colab?
==============

Application that integrates existing systems to represent the contributions of the members through:

* The amendments to the Wiki trac system.

* Changes to the trac system code.

* Discussions at the mailman list.

* And other systems in the community.



Features
========

* Developed by Interlegis Communities http://colab.interlegis.leg.br/

* Written in Python http://python.org/

* Built with Django Web Framework https://www.djangoproject.com/

* Search engine with Solr https://lucene.apache.org/solr/



Installation
============

First install the dependencies and than the project it self:

.. code-block::

  pip install -e .

Development environment
-----------------------

You must install vagrant to set up the development environment. With vagrant available you should run:

.. code-block::

  vagrant up

During the process you should choose the vagrant box that you want to use. In the end you should have a virtual machine with development environment set up.



Running Colab
=============

To run Colab with development server you will have to:

1- Log in virtual machine:

.. code-block::

  vagrant ssh
  
2- Use colab virtualenv:

.. code-block::

  workon colab
  
3- Run the development server: 

.. code-block::

  colab-admin runserver 0.0.0.0:8000

Now you can access colab in your browser via http://localhost:8000

**NOTE**: In case you want to keep the configuration file else where just set the 
desired location in environment variable **COLAB_SETTINGS**.

About test
==========

How to write a test
--------------------
Inside of each folder on /vagrant/colab/<folder> you can create a folder called
"tests" and inside of it implements the code for test each file. Remember that you should create __init__.py file.
 
How to run the tests
--------------------

Follow the steps below:

1- Log in virtual machine:

.. code-block::

  vagrant ssh

2- Use colab virtualenv:

.. code-block::

  workon colab

3- Enter into colab source code directory:

.. code-block::

  cd /vagrant

4- Run tests with setup.py:

.. code-block::

  python setup.py test

How to run Acceptance Tests
---------------------------

Follow the steps below to run the acceptance tests. 

1- Log in virtual machine:

1.1 - To run without opening a graphic interface 

.. code-block::

  vagrant ssh

1.2 - To run opening a graphic interface 

.. code-block::

  vagrant ssh -- -X

2- Use colab virtualenv:

.. code-block::

  workon colab

3- Enter into colab source code directory:

.. code-block::

  cd /vagrant

4- Run all the acceptance tests with:

.. code-block::

  COLAB_SETTINGS=tests/colab_settings.py colab-admin behave

4.1 To run without opening a browser:
.. code-block::

  COLAB_SETTINGS=tests/colab_settings.py xvfb-run -a colab-admin behave 

4.2 To run a specific feature:

.. code-block::

  COLAB_SETTINGS=tests/colab_settings.py colab-admin behave /path/to/features/file.feature

