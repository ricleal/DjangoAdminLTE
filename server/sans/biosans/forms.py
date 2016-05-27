'''
Created on Jan 8, 2016

@author: rhf
'''
from django.forms import ModelForm

from .models import BIOSANSConfiguration

class ConfigurationForm(ModelForm):
    class Meta:
        model = BIOSANSConfiguration
        exclude = ['user','instrument']
