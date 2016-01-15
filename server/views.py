"""
    User management
"""

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.conf import settings

import urllib
import os

class Index(LoginRequiredMixin,TemplateView):
    template_name = 'index.html'
    

def dirlist(request, instrument):
    '''
    This wil be called by the server side file browser
    
    '''
    r = ['<ul class="jqueryFileTree" style="display: none;">']
    prefix = settings.SERVER_FILES_PREFIX%({"instrument":instrument})
    try:
        r = ['<ul class="jqueryFileTree" style="display: none;">']
        #d = urllib.unquote(request.POST.get('dir', '/tmp'))
        d = prefix
        for f in os.listdir(d):
            ff = os.path.join(d, f)
            if os.path.isdir(ff):
                r.append(
                    '<li class="directory collapsed"><a href="#" rel="%s/">%s</a></li>' % (ff, f))
            else:
                e = os.path.splitext(f)[1][1:]  # get .ext and remove dot
                r.append(
                    '<li class="file ext_%s"><a href="#" rel="%s">%s</a></li>' % (e, ff, f))
        r.append('</ul>')
    except Exception, e:
        r.append('Could not load directory: %s' % str(e))
    r.append('</ul>')
    return HttpResponse(''.join(r))