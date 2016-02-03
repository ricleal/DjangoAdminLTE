"""
    Util
"""

from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
import urllib
import os
import logging

logger = logging.getLogger('util.views')

@login_required
def dirlist(request, instrument):
    '''
    This wil be called by the server side file browser

    '''
    default_dir = settings.SERVER_FILES_PREFIX%({"instrument":instrument})
    
    r = ['<ul class="jqueryFileTree" style="display: none;">']
    try:
        r = ['<ul class="jqueryFileTree" style="display: none;">']
        post_dir = urllib.unquote(request.POST.get('dir'))
        if post_dir == '/':
            d = default_dir
        else:
            d = post_dir
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
        logger.exception(e)
    r.append('</ul>')
    return HttpResponse(''.join(r))