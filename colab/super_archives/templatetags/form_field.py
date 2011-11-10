from django import template

def render_form_field(parser, token):
    variables = token.split_contents()

    if len(variables) == 2:
        tag_name, form_field = variables
        default_value = 'None'
    elif len(variables) == 3:
        tag_name, form_field, default_value = variables
    else:
        raise TemplateSyntaxError
        
    return RenderFormField(form_field, default_value)

    
class RenderFormField(template.Node):
    
    def __init__(self, form_field, default_value):
        self.form_field_nocontext = template.Variable(form_field)
        self.default_value_nocontext = template.Variable(default_value)
        
    def render(self, context):
        editable = context.get('editable', True)

        class_ = ''
        errors = ''
        form_field_tag = ''
        form_field = self.form_field_nocontext.resolve(context)
 
        if form_field.errors:
            class_ += 'error'
        if form_field.field.required:
            class_ += ' required'    
        if form_field.errors:
            errors = '<br/>' + form_field.errors.as_text()
        
        try:
            default_value = self.default_value_nocontext.resolve(context)
        except template.VariableDoesNotExist:
            pass
        
        if editable:
            form_field_tag = '<br/>' + str(form_field)
        else:
            form_field_tag = default_value
                
        return """<p class="%s">%s: %s %s</p>""" % (
            class_, 
            form_field.label_tag(), 
            form_field_tag,
            errors
        )
        
register = template.Library()
register.tag('render_form_field', render_form_field)