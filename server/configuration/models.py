from __future__ import unicode_literals

from django.db import models

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
    ipts = models.CharField(max_length=16)
    title = models.CharField(max_length=256)
    label = models.CharField(max_length=1, choices=LABEL_TYPE_CHOICES, default='0')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

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
    
class SANSScans(models.Model):
    title = models.CharField(max_length=256)
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
    pass
