from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from server.catalog.models import Instrument
from django.utils.translation import ugettext_lazy as _

import logging
logger = logging.getLogger('sans.models')

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


class EntryManager(models.Manager):
    '''
    Queries go here!!
    '''
    
    use_for_related_fields = True

    def visible_instruments(self, **kwargs):
        return self.filter(visible="True", **kwargs)
    
    def create_entries_from_handsontable(self, handsontable, reduction):
        '''
        Create entries based on the contensts of handsontable
        @param handsontable: It's a 2D array
        @param reduction: reduction object to associate with the created entries
        '''
        for row in handsontable:
            if any(row): #Row has some data
                keywords_args = { field : elem for elem,field in zip(row,Entry.get_field_names()) }
                logger.debug("Creating Entry object with: %s"%keywords_args)
                keywords_args['reduction']=reduction
                # The following is the same as: 
                # entry = Entry(**keywords_args)
                # entry.save(force_insert=True)
                self.create(**keywords_args)
                
                    

class Entry(models.Model):
    '''
    All Entries are Runs, except the description
    '''
    sample_scattering = models.CharField(max_length=256)
    sample_transmission = models.CharField(max_length=256)
    background_scattering = models.CharField(max_length=256)
    background_transmission = models.CharField(max_length=256)
    empty_beam = models.CharField(max_length=256)
    save_name = models.CharField(max_length=256, blank=True)
    
    # Manager
    objects = EntryManager()
    
    class Meta:
        abstract = True
        ordering = ["id"]
        verbose_name_plural = _("Entries")

    def __unicode__(self):
        return self.save_name, 
    
    def get_fields(self):
        '''
        @return: pairs key,values for all fields of this class
        '''
        return [(field.name, field.value_to_string(self)) for field in self._meta.fields]
    
    @staticmethod
    def get_field_titled_names():
        '''
        @return: field names as title for web display no unicode
        '''
        return [str(field.verbose_name.title()) for field in Entry._meta.fields]
    
    @staticmethod
    def get_field_names():
        '''
        @return: field names no unicode
        '''
        return [str(field.name) for field in Entry._meta.fields]




