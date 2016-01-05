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
        on_delete=models.CASCADE)  # , blank=True, null=True)
    owner = models.ForeignKey(User,
        on_delete=models.CASCADE)  # , blank=True, null=True)
    ipts = models.CharField(max_length=16, blank=True, null=True,)
    title = models.CharField(max_length=256, blank=True, null=True,)
    label = models.CharField(max_length=1, choices=LABEL_TYPE_CHOICES, default='0')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True
    def __unicode__(self):
        return self.title
    
    @models.permalink
    def get_absolute_url(self):
        return ('configuration_detail_detail', [self.pk])

    def get_fields(self):
        '''
        @return: pairs key,values for all fields of this class
        '''
        return [(field.name, field.value_to_string(self)) for field in self._meta.fields]
class Scan(models.Model):
    '''
    '''
    title = models.CharField(max_length=256, blank=True, null=True,)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True
    def __unicode__(self):
        return self.title
    
    def get_fields(self):
        '''
        @return: pairs key,values for all fields of this class
        '''
        return [(field.name, field.value_to_string(self)) for field in self._meta.fields]
#
# SANS Abstract
#

class SANSCommon(Configuration):
    dark_current_run = models.CharField(max_length=256, blank=True, null=True,)
    beam_center_run = models.CharField(max_length=256, blank=True, null=True,)
    class Meta:
            abstract = True

class SANSScans(Scan):
    sample_run = models.CharField(max_length=256)
    sample_transmission_run = models.CharField(max_length=256, blank=True, null=True,)
    background_run = models.CharField(max_length=256, blank=True, null=True,)
    background_transmission_run = models.CharField(max_length=256, blank=True, null=True,)
    transmission_run = models.CharField(max_length=256, blank=True, null=True,)
    class Meta:
        abstract = True

#
# BIOSANS
#
class BioSANSCommon(SANSCommon):
    empty_transmission_run = models.CharField(max_length=256, blank=True, null=True,)
    flood_field_run = models.CharField(max_length=256, blank=True, null=True,)
    
class BioSANSScan(SANSScans):
    # We can not have ForeignKey for abstract models. It has to be here!!
    configuration = models.ForeignKey(BioSANSCommon,
                on_delete=models.CASCADE,
                related_name="scan",
                related_query_name="scan",)

#
# EQSANS
#
class EQSANSCommon(SANSCommon):
    absolute_scale_factor = models.DecimalField(max_digits=10,decimal_places=2,default=1.0)
    sample_thickness = models.DecimalField(max_digits=10,decimal_places=2,default=1.0)
    sample_aperture_diameter = models.DecimalField(max_digits=10,decimal_places=2,default=10.0)
    sensitivity_run  = models.CharField(max_length=256, blank=True, null=True,)
    sensitivity_min = models.DecimalField(max_digits=10,decimal_places=2,default=0.4)
    sensitivity_max = models.DecimalField(max_digits=10,decimal_places=2,default=2.0)
    direct_beam_run = models.CharField(max_length=256, blank=True, null=True,)
    mask_run = models.CharField(max_length=256, blank=True, null=True,)
    
class EQSANSScan(SANSScans):
    # We can not have ForeignKey for abstract models. It has to be here!!
    configuration = models.ForeignKey(EQSANSCommon,
                on_delete=models.CASCADE,
                related_name="scan",
                related_query_name="scan",)

