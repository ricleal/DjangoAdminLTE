from django.shortcuts import render


from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin


import logging

logger = logging.getLogger('biosans')


class ConfigurationList(LoginRequiredMixin,ListView):
    '''
    List all configurations.
    '''
    template_name = 'configuration/configuration_list.html'


class ConfigurationDetail(LoginRequiredMixin,DetailView):
    '''
    Detail of a configuration
    '''
    template_name = 'configuration/configuration_detail.html'
    
class ConfigurationCreate(LoginRequiredMixin,CreateView):
    '''
    Detail of a configuration
    '''
    template_name = 'configuration/configuration_detail.html'