import re
from django import template
from django.conf import settings

register = template.Library()
numeric_test = re.compile("^\d+$")

def getattribute(value, arg):
    """Gets an attribute of an object dynamically from a string name"""

    if hasattr(value, str(arg)):
        return_value = getattr(value, arg)
    elif hasattr(value, 'has_key') and value.has_key(arg):
        return_value = value[arg]
    elif numeric_test.match(str(arg)) and len(value) > int(arg):
        return_value = value[int(arg)]
    else:
        return_value = False
    if return_value == "NULL":
        return_value = False
    return(return_value)


register.filter('getattribute', getattribute)