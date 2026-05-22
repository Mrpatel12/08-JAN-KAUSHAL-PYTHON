from django import template

register = template.Library()


@register.filter(name='add_class')
def add_class(bound_field, css_class):
    """Return the field rendered with the given css class added to its widget."""
    try:
        return bound_field.as_widget(attrs={"class": css_class})
    except Exception:
        return bound_field
