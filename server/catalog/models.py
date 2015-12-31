from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Instrument(models.Model):
    beamline = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=256)
    visible = models.BooleanField(default=True)

    def __unicode__(self):
            return self.name
