from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from server.catalog.models import Instrument

class Job(models.Model):
    '''
    Job will have a foreign key to here
    The same configuration can launch multiple jobs!
    '''
    
    MY_STATUS = ((0,'NOT_SUBMITTED'), (1, 'SUBMITTED'),)
    FERMI_STATUS = ((3,'RUNNING'),
                    (4,'QUEUED'), 
                    (5,'COMPLETED'), 
                    (6,'REMOVED'), 
                    (7,'DEFERRED'), 
                    (8,'IDLE'), 
                    (9,'UNKNOWN'),)
    
    status = models.IntegerField(choices =  MY_STATUS + FERMI_STATUS, default = MY_STATUS[0])
    
    script = models.TextField(max_length=10240)
    
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE,
                                   related_name="job_instruments",
                                   related_query_name="job_instrument",)
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name="job_users",
                             related_query_name="job_user",)
    
    # Generic Relation for a reduction
    # Table Job will have 2 fields which are foreign keys to other tales: table_name, table.pk
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    class Meta:
        ordering = ["id"]

    def __unicode__(self):
        return "%s - %s" % (self.id, self.status)
    
    @models.permalink
    def get_absolute_url(self):
        return ('jobs:job_detail', [self.pk])
    
    def get_field_titled_names_and_values(self):
        '''
        Does not display related fields (i.e. FK)
        @return: field names as title and values for web display no unicode
        '''
        return [ (str(field.verbose_name.title()), field.value_to_string(self)) for field in self._meta.fields if not field.is_relation]

