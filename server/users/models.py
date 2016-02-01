from __future__ import unicode_literals

from django.db import models
from django.conf import settings

#from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin

from server.catalog.models import Instrument


class User(AbstractBaseUser, PermissionsMixin):
    '''
    This will overwrite the default user model
    '''
    username = models.CharField(max_length=40, unique=True, db_index=True,)
    email = models.EmailField(max_length=100,unique=True,blank=True)
    fullname = models.CharField(max_length=100, blank=True,  verbose_name = _("Full Name"))
    address  = models.CharField(max_length=250, blank=True)
    
    date_joined = models.DateField(auto_now=True)
    
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def get_full_name(self):
        return self.fullname

    def get_short_name(self):
        return self.username
    
    def __unicode__(self):
        return self.username
    

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name="profile", related_query_name="profile",)
    
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE,)
    home_institution = models.CharField(max_length=200, blank=True, null=True)
    
    def __unicode__(self):
        return  _("%s :: %s.") %  (self.user, self.instrument)
       
    # Meta
    class Meta:
        verbose_name = _("User Profile")
