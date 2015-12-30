from django.contrib.auth.signals import user_logged_in
import hashlib

#
GRAVATAR_URL = "https://www.gravatar.com/avatar/"

def build_avatar_link(sender, user, request, **kwargs):
    '''
    Adds  a gravatar key,value to the session object
    '''
    if hasattr(request, 'user') and request.user.is_authenticated():
        gravatar_url = GRAVATAR_URL+hashlib.md5(request.user.email).hexdigest()+'?d=identicon'
        request.session['gravatar_url'] = gravatar_url

user_logged_in.connect(build_avatar_link)
