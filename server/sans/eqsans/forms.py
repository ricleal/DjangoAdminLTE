'''
Created on Jan 8, 2016

@author: rhf
'''
from django.forms import ModelForm

from .models import EQSANSConfiguration

class ConfigurationForm(ModelForm):
    class Meta:
        model = EQSANSConfiguration
        exclude = ['user','instrument']