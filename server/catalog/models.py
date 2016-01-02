from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Instrument(models.Model):
    beamline = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=32, unique=True)
    description = models.CharField(max_length=256)
    # We can have instruments but they will be invisble in the web page
    visible = models.BooleanField(default=True)

    def __unicode__(self):
            return self.name
