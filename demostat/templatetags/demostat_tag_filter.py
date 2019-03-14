from django import template

register = template.Library()

def generate_qs(dict):
    out = ''
    for value in dict['tag']:
            out += '&tag=' + str(value)

    if dict['org']:
        out += '&org=' + str(dict['org'])

    if out:
        return '?' + out[1:]
    else:
        return ''

@register.simple_tag
def tf_generate_qs(**dict):
    return generate_qs(dict)

@register.simple_tag
def tf_generate_qs_without(value, **dict):
    if value in dict['tag']:
        dict['tag'].remove(value)
    return generate_qs(dict)
