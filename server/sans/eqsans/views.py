from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import EQSANSConfiguration

import logging

logger = logging.getLogger('eqsans')


class ConfigurationList(LoginRequiredMixin, ListView):
    '''
    List all configurations.
    '''
    template_name = 'sans/eqsans/configuration_list.html'
    model = EQSANSConfiguration

class ConfigurationDetail(LoginRequiredMixin, DetailView):
    '''
    Detail of a configuration
    '''
    template_name = 'sans/eqsans/configuration_detail.html'
    model = EQSANSConfiguration

class ConfigurationCreate(LoginRequiredMixin, CreateView):
    '''
    Detail of a configuration
    '''
    template_name = 'sans/eqsans/configuration_form.html'
    model = EQSANSConfiguration

class ConfigurationUpdate(LoginRequiredMixin, UpdateView):
    '''
    Detail of a configuration
    '''
    template_name = 'sans/eqsans/configuration_form.html'
    model = EQSANSConfiguration