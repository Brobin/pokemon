from django import template


register = template.Library()


@register.filter(name='add_class')
def add_class(field, cls):
    return field.as_widget(attrs={"class": cls})


@register.simple_tag(name='url_replace')
def url_replace(request, field, value):
    params = request.GET.copy()
    params[field] = value
    return params.urlencode()
