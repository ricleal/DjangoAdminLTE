from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

from .models import EQSANSConfiguration
from .forms import ConfigurationForm
from server.catalog.models import Instrument

from pprint import pformat
import logging


logger = logging.getLogger('sans.eqsans')

instrument_name = "EQ-SANS"

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
    
#     def render_to_response(self, context, **response_kwargs):
#         '''
#         Just to log the context
#         '''
#         logger.debug(pformat(context))
#         return super(ConfigurationDetail, self).render_to_response(context, **response_kwargs)
        

class ConfigurationCreate(LoginRequiredMixin, CreateView):
    '''
    Detail of a configuration
    '''
    template_name = 'sans/eqsans/configuration_form.html'
    form_class = ConfigurationForm
    
    def get_initial(self):
        # Get the initial dictionary from the superclass method
        initial = super(ConfigurationCreate, self).get_initial()
        # Copy the dictionary so we don't accidentally change a mutable dict
        initial = initial.copy()
        initial['user'] = self.request.user.pk
        initial['instrument'] = get_object_or_404(Instrument, name=instrument_name)
        return initial

class ConfigurationUpdate(LoginRequiredMixin, UpdateView):
    '''
    Detail of a configuration
    '''
    template_name = 'sans/eqsans/configuration_form.html'
    form_class = ConfigurationForm
    model = EQSANSConfiguration