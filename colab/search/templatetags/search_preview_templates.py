from django import template


register = template.Library()

@register.assignment_tag
def get_search_preview_templates(model_indexed):
    app_type = model_indexed.type
    app_name = ""

    if app_type in "user":
        app_name = "accounts"
    elif app_type in "thread":
        app_name = "superarchives"
    else:
        app_name, app_type = app_type.split("_",1)

    return "{}/{}_search_preview.html".format(app_name, app_type)
