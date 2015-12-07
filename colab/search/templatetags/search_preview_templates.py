from django import template


register = template.Library()


@register.assignment_tag
def get_search_preview_templates(model_indexed):
    app_type = model_indexed.type

    return "search/{}_search_preview.html".format(app_type)


@register.assignment_tag
def get_dashboard_search_preview_templates(model_indexed):
    app_type = model_indexed.type

    return "dashboard/{}_search_preview.html".format(app_type)
