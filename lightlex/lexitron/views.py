# vim: ai ts=4 sts=4 et sw=4

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

import os
from pylexitron import Lexitron

def lookup(request, lookup_str=''):
    if request.POST.has_key('lookup_str') and request.POST['lookup_str'] != '':
        return HttpResponseRedirect('/%s' % request.POST['lookup_str'])

#    lookup_str = unicode(lookup_str)
    if lookup_str.startswith('/'):
        lookup_str = lookup_str[1:]
    d = {'lookup_str': lookup_str.lower()}

    if d['lookup_str'] == '':
        return render_to_response('index.html')
    else:
        lexitron = Lexitron('%s/..' % os.path.dirname(__file__))

        results = lexitron.search(d['lookup_str'])
        if results['items']:
            items = []
            for i in results['items']:
                t = {}
                if results['type'] == 'et':
                    t.update({'tentry': i[3]})
                    t.update({'ecat': i[4]})
                    t.update({'ethai': i[5]})
                    t.update({'eant': i[6]})
                    t.update({'esyn': i[7]})
                else: # te
                    t.update({'eentry': i[3]})
                    t.update({'tcat': i[4]})
                    t.update({'tenglish': i[5]})
                    t.update({'tant': i[6]})
                    t.update({'tsyn': i[7]})
                    t.update({'tsample': i[8]})
                    t.update({'tdef': i[9]})
                    t.update({'tnum': i[10]})
                items.append(t)
            template_name = 'lookup_%s.html' % results['type']
            d.update({'items': items, 'senses': results['senses']})
        else:
            if len(d['lookup_str']) >= 4:
                results = lexitron.list(d['lookup_str'])
                template_name = 'list.html'
                d['items'] = results['items']
            else:
                template_name = 'error.html'
                d['short_message'] = 'Not Found'
                d['long_message'] = 'To see a suggestion list, please enter at least 4 characters.'
        return render_to_response(template_name, d)

