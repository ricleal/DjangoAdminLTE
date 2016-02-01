from __future__ import unicode_literals

from django.db import models
from django.contrib.auth import get_user_model
from server.catalog.models import Instrument
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

import logging
logger = logging.getLogger('sans.models')

'''

Abstract models for SANS

Configuration - 1 to many - Reductions
Reduction - 1 to many - Entries

'''

class ConfigurationManager(models.Manager):
    '''
    Configuration go here!!
    '''

    use_for_related_fields = True

    def clone(self, pk):
        '''
        Clone an object and returns 
        '''
        obj = self.get(id = pk)
        obj.pk = None # setting to None, clones the object!
        obj.save() 
        return obj
    
    def clone_and_assign_new_user(self,pk,new_user):
        '''
        '''
        obj = self.get(id = pk)
        obj.pk = None # setting to None, clones the object!
        obj.user = get_user_model().objects.get(username= new_user)
        obj.save() 
        return obj
        
        
        

class Configuration(models.Model):
    '''
    Job will have a foreign key to here
    The same configuration can launch multiple jobs!
    '''

    title = models.CharField(max_length=256, blank=True)
    
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE,
                                   related_name="instruments",
                                   related_query_name="instrument",)  # , blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name="users",
                             related_query_name="user",)  # , blank=True, null=True)
    
    # Manager
    objects = ConfigurationManager()

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

    def get_field_titled_names_and_values(self):
        '''
        Does not display related fields (i.e. FK)
        @return: field names as title and values for web display no unicode
        '''
        return [ (str(field.verbose_name.title()), field.value_to_string(self)) for field in self._meta.fields if not field.is_relation]

class ReductionManager(models.Manager):
    '''
    Configuration go here!!
    '''

    use_for_related_fields = True

    def clone(self, pk):
        '''
        Clones the Reduction object and related entries
        '''
        obj = self.get(id = pk)
        old_title = obj.title
        # Let's clone the related entries
        new_entries =[]
        for e in obj.entries.all():
            e.pk = None
            e.save()
            new_entries.append(e)
            
        obj.pk = None # setting to None, clones the object!
        obj.save()
        obj.entries = new_entries
        obj.title = "%s (copy)"%old_title
        obj.save()
        return obj
    
class Reduction(models.Model):
    '''
    '''
    title = models.CharField(max_length=256, blank=True)
    ipts = models.CharField(max_length=16, blank=True)
    
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    # Manager
    objects = ReductionManager()
    
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
    
    def get_field_titled_names_and_values(self):
        '''
        Does not display related fields (i.e. FK)
        @return: field names as title and values for web display no unicode
        '''
        return [ (str(field.verbose_name.title()), field.value_to_string(self)) for field in self._meta.fields if not field.is_relation]

