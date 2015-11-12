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
            def generate_content(self, **kwargs):
                # process HTML content
                self.content = processed_content

To add the widget in a view check the Widgets section in User Documentation.
To use a widget in the templates, you have to use the ``import_widget`` tag inside the ``html`` block.
This way, the kwargs parameter will have a ``context`` key from the ``html``.
You can also set the variable that the widgets of an area will be imported.
Or you can use the default name, which is ``widgets_area_name``.
For example, in the ``profile`` area the variable name is ``widgets_profile``.
This variable will be inserted directly in the page ``context``.

.. code-block:: python

    {% load widgets_tag %}

    {% block html %}
       {% import_widgets 'profile' %}
       {{ block.super }}
    {% endblock %}

    {# example of how to use #}
    {% block head %}
      {{ block.super }}

      {% for widget in widgets_profile %}
        {{ widget.get_header }}
      {% endfor %}

    {% endblock %}


.. warning::

    Warning! Remember to use the tag ``{{ block.super }}`` inside the html block. Otherwise, the page will appear blank.
