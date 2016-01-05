from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import UserProfile

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

# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_profile_handler(sender, instance, created, **kwargs):
#     '''
#     Once user logs in this is called!
#     It will create a user profile.
#     '''
#     print "***********************************"
#     if not created:
#         return
#     # Create the profile object, only if it is newly created
# 
#     profile = UserProfile(user=instance)
#     profile.save()