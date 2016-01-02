from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from server.catalog.models import Instrument
# Create your models here.

class Configuration(models.Model):
    '''
    Job will have a foreign key to here
    The same configuration can launch multiple jobs!
    '''

    LABEL_TYPE_CHOICES = (
        ('0', ''),
        ('1', 'Template'),
        ('2', 'TODO 1'),
        ('3', 'TODO 2'),
    )
    instrument = models.ForeignKey(Instrument,
        on_delete=models.CASCADE ) #, blank=True, null=True)
    owner = models.ForeignKey(User,
        on_delete=models.CASCADE ) #, blank=True, null=True)
    ipts = models.CharField(max_length=16)
    title = models.CharField(max_length=256)
    label = models.CharField(max_length=1, choices=LABEL_TYPE_CHOICES, default='0')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True
    def __unicode__(self):
            return self.title

class Scan(models.Model):
    '''
    '''
    title = models.CharField(max_length=256)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True
    def __unicode__(self):
            return self.title
#
# SANS Abstract
#

class SANSCommon(Configuration):
    empty_transmission_run = models.CharField(max_length=256)
    dark_current_run = models.CharField(max_length=256)
    flood_field_run = models.CharField(max_length=256)
    beam_center_run = models.CharField(max_length=256)
    class Meta:
            abstract = True

class SANSScans(Scan):
    data_run = models.CharField(max_length=256)
    background_run = models.CharField(max_length=256)
    transmission_run = models.CharField(max_length=256)
    class Meta:
        abstract = True

#
# BIOSANS
#
class BioSANSCommon(SANSCommon):
    pass

class BioSANSScan(SANSScans):
    # We can not have ForeignKey for abstract models. It has to be here!!
    configuration = models.ForeignKey(BioSANSCommon,
                on_delete=models.CASCADE )
