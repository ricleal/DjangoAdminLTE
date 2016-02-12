from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.text import slugify

from server.catalog.models import Instrument
from .remote import communication as remote

import logging

logger = logging.getLogger('jobs.models')

class TransactionManager(models.Manager):
    '''
    Configuration go here!!
    '''

    use_for_related_fields = True
    
    def start_transaction(self,request,title):
        '''
        start the transaction in remote and creates the transaction object in the DB
        '''
        cookie = request.session["remote"]
        _, transaction_remote = remote.start_transaction(cookie)
        if transaction_remote:
            #"To create and save an object in a single step, use the create() method."
            transaction = self.create(
                title = title, # same title as the job!
                remote_id = transaction_remote["TransID"],
                remote_directory = transaction_remote["Directory"],
            )
            return transaction
        return None
    
    def file_listing(self, request, transaction):
        cookie = request.session["remote"]
        success, files_json = remote.file_listing(cookie, transaction.remote_id)
        if success:
            return files_json["Files"]
        else:
            return None
    
    def download(self, request, transaction, filename):
        logger.debug("Downloading %s."%filename)
        cookie = request.session["remote"]
        success, file_content = remote.download(cookie, transaction.remote_id, filename)
        if success:
            return file_content
        else:
            return None
    
    
        
        
class Transaction(models.Model):
    '''
    A transaction can have multiple jobs
    Multiple jobs run in the same transaction folder
    I guess only one job per transaction for SANS
    '''

    title = models.CharField(max_length=256)

    # Those are returned when a transaction is created
    remote_id = models.IntegerField()
    remote_directory = models.CharField(max_length=256)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    # Manager
    objects = TransactionManager()
    
    class Meta:
        ordering = ["-id"]

    def __unicode__(self):
        return "Remote id: %8d :: %s" % (self.remote_id,self.title)

class JobManager(models.Manager):
    '''
    Configuration go here!!
    '''

    use_for_related_fields = True
    
    def clone(self, obj):
        '''
        Clone an object and returns 
        '''
        obj.pk = None # setting to None, clones the object!
        obj.title = obj.title + " (copy)"
        obj.save() 
        return obj
    
    def submit_job(self, request, transaction, job):
        '''
        @param obj: Job instance
        '''
        if job.local_status > 0: #It was submitted already!
            job = self.clone(job)
        job.transaction = transaction
        
        cookie = request.session["remote"]
        success, resp = remote.submit_job(cookie, transaction.remote_id, 
                                 {'run.py': job.script}, slugify(job.title), 
                                 job.number_of_nodes, job.cores_per_node)
        if success:
            job.remote_id = resp['JobID']
            job.local_status = 1
            job.save()
            return job
        else:
            job.delete()
            transaction.delete()
            return None
    
    def query_job(self, request, job):
        cookie = request.session["remote"]
        success, resp = remote.query_job(cookie, job.remote_id)
        if success:
            try:
                d = resp.values()[0]
                job.remote_submit_date = d['SubmitDate']
                job.remote_start_date = d['StartDate']
                job.remote_complete_date = d['CompletionDate']
                job.remote_status = job.assign_remote_status(d['JobStatus'])
                job.save()
                return job                
            except Exception , e:
                logger.exception(e)
        return None
    
    def delete_job(self, request, job):
        cookie = request.session["remote"]
        success, _ = remote.abort_job(cookie, job.remote_id)
        return success
        
class Job(models.Model):
    '''
    Job will have a foreign key to here
    The same configuration can launch multiple jobs!
    '''
    
    def assign_remote_status(self,status):
        for k,v in self.REMOTE_STATUS:
            if v == status:
                return k
        return None

    # status when the job is created or sent to the cluster
    LOCAL_STATUS = ((0,'NOT_SUBMITTED'), (1, 'SUBMITTED'),)
    # Remote job status when it is queried
    REMOTE_STATUS = ((3,'RUNNING'),
                    (4,'QUEUED'),
                    (5,'COMPLETED'),
                    (6,'REMOVED'),
                    (7,'DEFERRED'),
                    (8,'IDLE'),
                    (9,'UNKNOWN'),)

    title = models.CharField(max_length=256)

    # script is generated and saved here
    script = models.TextField(max_length=10240)
    # Set to true if the user changes the generated script
    script_changed = models.BooleanField(default = False)
    
    number_of_nodes = models.IntegerField(default=1, validators=[
            MaxValueValidator(4),
            MinValueValidator(1)
        ])
    cores_per_node = models.IntegerField(default=4, validators=[
            MaxValueValidator(8),
            MinValueValidator(1)
        ])    

    local_status = models.IntegerField(choices =  LOCAL_STATUS, default = 0)
    # blank=True: user is allowed to omit the value in a form, null = True because it's an int in the DB
    remote_status = models.IntegerField(choices =  REMOTE_STATUS, blank=True, null = True)

    remote_id =  models.IntegerField( blank=True, null = True)
    
    # Those represent the remote job: "CompletionDate", "StartDate", "SubmitDate":
    remote_submit_date = models.DateTimeField(blank=True, null = True)
    remote_start_date = models.DateTimeField(blank=True, null = True)
    remote_complete_date = models.DateTimeField(blank=True, null = True)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    # Generic Relation for a reduction
    # Table Job will have 2 fields which are foreign keys to other tales: table_name, table.pk
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # A form can exist without a transaction: null = True
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, null = True,
                             related_name="transactions",
                             related_query_name="transaction",)

    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE,
                                   related_name="job_instruments",
                                   related_query_name="job_instrument",)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name="job_users",
                             related_query_name="job_user",)
    
    # Manager
    objects = JobManager()
    
    class Meta:
        ordering = ["-id"]

    def __unicode__(self):
        return "Remote Id: %s :: %s: %s" % (self.remote_id, self.title, self.get_local_status_display())

    @models.permalink
    def get_absolute_url(self):
        return ('jobs:job_detail', [self.pk])

    def get_field_titled_names_and_values(self):
        '''
        Does not display related fields (i.e. FK)
        @return: field names as title and values for web display no unicode
        '''
        return [ (str(field.verbose_name.title()), field.value_to_string(self)) for field in self._meta.fields if not field.is_relation]

    
