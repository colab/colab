from django import template
from django import forms

def render_form_field(parser, token):
    variables = token.split_contents()

    if len(variables) == 2:
        tag_name, form_field = variables
        default_value = 'None'
    elif len(variables) == 3:
        tag_name, form_field, default_value = variables
    else:
        raise template.TemplateSyntaxError
        
    return RenderFormField(form_field, default_value)

    
class RenderFormField(template.Node):
    
    def __init__(self, form_field, default_value):
        self.form_field_nocontext = template.Variable(form_field)
        self.default_value_nocontext = template.Variable(default_value)
        
    def render(self, context):
        editable = context.get('editable', True)

        class_ = u''
        errors = u''
        form_field_tag = u''
        try:
            form_field = self.form_field_nocontext.resolve(context)
        except template.VariableDoesNotExist:
            return u''
 
        if form_field.errors:
            class_ += u'error'
        if form_field.field.required:
            class_ += u' required'    
        if form_field.errors:
            errors = u'<br/>' + form_field.errors.as_text()
        
        try:
            default_value = self.default_value_nocontext.resolve(context)
        except template.VariableDoesNotExist:
            default_value = u''
        
        if editable:
            form_field_tag = u'<br/>' + unicode(form_field)
        elif isinstance(form_field.field, forms.URLField):
            form_field_tag = u"""<a href="%s" target="_blank">%s</a>""" % (
                default_value, default_value)
        else:
            form_field_tag = default_value
                
        return u"""<p class="%s">%s: %s %s</p>""" % (
            class_, 
            form_field.label_tag(), 
            form_field_tag,
            errors
        )

 
register = template.Library()
register.tag('render_form_field', render_form_field)
