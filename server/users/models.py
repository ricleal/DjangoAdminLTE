from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from server.catalog.models import Instrument

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="profile",
                related_query_name="profile",)
    instrument = models.OneToOneField(Instrument, on_delete=models.CASCADE,)
    home_institution = models.CharField(max_length=200, blank=True, null=True)