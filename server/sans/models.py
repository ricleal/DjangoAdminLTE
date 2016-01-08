from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from server.catalog.models import Instrument
from django.utils.translation import ugettext_lazy as _

from .eqsans import *


'''

Abstract models for SANS

Configuration - 1 to many - Reductions
Reduction - 1 to many - Entries

'''

class Configuration(models.Model):
    '''
    Job will have a foreign key to here
    The same configuration can launch multiple jobs!
    '''

    ipts = models.CharField(max_length=16, blank=True, null=True,)
    title = models.CharField(max_length=256, blank=True, null=True,)
    dark_current_run = models.CharField(max_length=256, blank=True, null=True,)
    beam_center_run = models.CharField(max_length=256, blank=True, null=True,)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE,
                                   related_name="instrument",
                                   related_query_name="instrument",)  # , blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="user",
                             related_query_name="user",)  # , blank=True, null=True)
    
    class Meta:
        abstract = True
        ordering = ["id"]
    
    def __unicode__(self):
        return self.title

    def get_fields(self):
        '''
        @return: pairs key,values for all fields of this class
        '''
        return [(field.name, field.value_to_string(self)) for field in self._meta.fields]

class Reduction(models.Model):
    '''
    '''
    title = models.CharField(max_length=256, blank=True, null=True,)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["id"]
        
    def __unicode__(self):
        return self.title
    
    def get_fields(self):
        '''
        @return: pairs key,values for all fields of this class
        '''
        return [(field.name, field.value_to_string(self)) for field in self._meta.fields]

class Entry(models.Model):
    '''
    '''
    
    sample_run = models.CharField(max_length=256)
    sample_transmission_run = models.CharField(max_length=256, blank=True, null=True,)
    background_run = models.CharField(max_length=256, blank=True, null=True,)
    background_transmission_run = models.CharField(max_length=256, blank=True, null=True,)
    transmission_run = models.CharField(max_length=256, blank=True, null=True,)
    description = models.CharField(max_length=256, blank=True, null=True,)
    
    class Meta:
        abstract = True
        ordering = ["id"]
        verbose_name_plural = _("Entries")

    def __unicode__(self):
        return self.description
    
    def get_fields(self):
        '''
        @return: pairs key,values for all fields of this class
        '''
        return [(field.name, field.value_to_string(self)) for field in self._meta.fields]



