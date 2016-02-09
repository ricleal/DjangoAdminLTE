'''
Created on Jan 8, 2016

@author: rhf
'''
from django import forms

from .models import Transaction, Job

class JobForm(forms.ModelForm):
    '''
    This will only present the title and the script
    '''
    class Meta:
        model = Job
        # Transaction excluded. It will be created after fermi transaction
        exclude = ['transaction', 'remote_submit_date','remote_start_date',
            'remote_complete_date']
        # All hidden: prepopulated from the URL
        widgets = {
            'script': forms.HiddenInput(),
            'script_changed': forms.HiddenInput(),
            'local_status': forms.HiddenInput(),
            'remote_status': forms.HiddenInput(),
            'content_type': forms.HiddenInput(),
            'object_id': forms.HiddenInput(),
        }
