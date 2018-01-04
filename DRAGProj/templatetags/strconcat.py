from django import template

"""
An extension module defining a filter for in Django html templates.

    Author:
        James
        
    Version:
        1.0.0
        
    See:
        django.template
"""

register = template.Library()  # Register any declared filters in the library.


@register.filter
def strconcat(string, anotherstring):
    """
    Concatenates strings with each other in the Django templating language.

    Args:
        string (:obj:`str`): The first string to combine.
        anotherstring (:obj:`str`): The second string to combine.

    Returns:
        :obj:`str`: The concatenation of the two strings.
    """
    return str(string) + str(anotherstring)
