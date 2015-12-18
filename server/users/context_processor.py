'''
Created on Dec 18, 2015

@author: rhf
'''
from django.conf import settings

import hashlib

def build_avatar_link(request):
    if request.user.is_authenticated():
        if hasattr(settings, 'GRAVATAR_URL'):
            gravatar_url = settings.GRAVATAR_URL+hashlib.md5(request.user.email).hexdigest()+'?d=identicon'
            return {'gravatar_url' :  gravatar_url}
    return {}

def user(request):
    out = {}
    out.update(build_avatar_link(request))
    print out
    return out