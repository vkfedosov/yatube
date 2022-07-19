from django import template

register = template.Library()


@register.filter
def addclass(field, css):

    context = {
        'class': css,
    }

    return field.as_widget(attrs=context)
