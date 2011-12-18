from django import template

register = template.Library()

def _split_all(s):
    l = s.split(';')
    for m in l:
        r = m.split(',')
        if len(r) > 1:
            l.remove(m)
            l.extend(r)
    return l

@register.filter
def category(s):
    if s == 'N':
        return '<a href="/noun">noun</a>'
    if s == 'PRON':
        return '<a href="/pronoun">pronoun</a>'
    elif s == 'ADJ':
        return '<a href="/noun">adjective</a>'
    elif s == 'ADV':
        return '<a href="/noun">adverb</a>'
    elif s == 'V':
        return '<a href="/noun">verb</a>'
    elif s == 'VT':
        return '<a href="/noun">transitive verb</a>'
    elif s == 'VI':
        return '<a href="/noun">intransitive verb</a>'
    elif s == 'PHRV':
        return '<a href="/noun">phrasal verb</a>'
    elif s == 'SL':
        return '<a href="/noun">slang</a>'
    elif s == 'IDM':
        return '<a href="/idiom">idiom</a>'
    elif s == 'CONJ':
        return '<a href="/conjunction">conjunction</a>'
    elif s == 'PREP':
        return '<a href="/preposition">preposition</a>'
    elif s == 'INT':
        return '<a href="/interjection">interjection</a>'
    elif s == 'AUX':
        return '<a href="/auxiliary verb">auxiliary verb</a>'
    elif s == 'DET':
        return 'determinant'
    elif s == 'CLAS':
        return 'classifier'
    else:
        return s.lower()

@register.filter
def to_lookup_link(s):
    return '<a href="/%(s)s">%(s)s</a>' % {'s': s}

@register.filter
def str_lookup_links(s):
    return ', '.join(['<a href="/%(s)s">%(s)s</a>' % {'s': s} for s in [w.strip() for w in _split_all(s)]])

@register.filter
def list_lookup_links(l):
    s = ', '.join(['<a href="/%(s)s">%(s)s</a>' % {'s': s} for s in l])
    if s:
        return s
    else:
        return ''

