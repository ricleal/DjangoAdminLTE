'''
Created on Jan 8, 2016

@author: rhf
'''
from django import forms
from django.utils.text import slugify

from .models import Job

from .remote import communication as remote

class JobForm(forms.ModelForm):
    '''
    This will only present the title and the script
    '''
    class Meta:
        model = Job
        # Transaction excluded. It will be created after fermi transaction
        exclude = ['transaction', 'remote_submit_date','remote_start_date',
            'remote_complete_date', 'instrument', 'user']
        # All hidden: prepopulated from the URL
        widgets = {
            'script': forms.HiddenInput(),
            'script_changed': forms.HiddenInput(),
            'local_status': forms.HiddenInput(),
            'remote_status': forms.HiddenInput(),
            'content_type': forms.HiddenInput(),
            'object_id': forms.HiddenInput(),
            'remote_id': forms.HiddenInput(),
        }
    
#     def save(self, *args, **kwargs):
#         '''
#         I'm overriding this because I have no choice!
#         I need the request object and can't have access to it from the models
#         ideally this would be in the model!
#         
#         ## TODO:
#         Save used for both save and submit!!!
#         ## Find a way to change this
#         
#         '''
#         if not self.instance.pk:
#             #This code only happens if the objects is
#             #not in the database yet. Otherwise it would have pk
#             cookie = self.request.session["remote"]
#             resp = remote.submit_job(self.request, cookie, self.instance.transaction.remote_id, 
#                                      {'run.py': self.instance.script}, 
#                                      slugify(self.instance.title), 
#                                      self.instance.number_of_nodes, self.instance.cores_per_node)
#             if resp:
#                 self.instance.remote_id = resp['JobID']
#             self.instance.local_status = 1
#         
#         return super(JobForm, self).save(*args, **kwargs)