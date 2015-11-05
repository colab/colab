Developer Documentation
==================

Getting Started
---------------
.. TODO

Widgets
-------

A widget is a piece of HTML that will be inserted in a specific spot in a page to render some view.

To create a new widget you need to extend the ``Widget`` class from ``colab.widgets``. In the child class you can override the methods below, but it is not mandatory:

.. attribute:: get_header

    This method should return the HTML code to be used in the page's head. So, it will extract the head content from the ``content``.

.. attribute:: get_body

    This method should return the HTML code to be used in the page's body. So, it will extract the body content from the ``content``.

.. attribute:: generate_content

    This method will set the ``content`` when the widget is requested by the ``WidgetManager``. The ``content`` contains a HTML code that will be rendered in the target page.

The Widget class has the following attributes:

.. attribute:: identifier

        The identifier has to be a unique string across the widgets.

.. attribute:: name

        The widget name is the string that will be used to render in the view, if needed.

Example Widget:

.. code-block:: python

        from colab.widgets.widget_manager import Widget

        class MyWidget(Widget):
            identifier = 'my_widget_id'
            name = 'My Widget'
            def generate_content(self, request):
                # process HTML content
                self.content = processed_content

To add the widget in a view check the Widgets section in User Documentation.
