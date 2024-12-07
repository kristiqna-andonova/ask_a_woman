from django import template

register = template.Library()

@register.filter
def add_class(value, arg):
    """
    Add a CSS class to an HTML element.
    Usage: {{ field|add_class:"my-class" }}
    """
    return value.as_widget(attrs={'class': arg})