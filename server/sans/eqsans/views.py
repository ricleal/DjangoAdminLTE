from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

from .models import EQSANSConfiguration, EQSANSReduction
from .forms import ConfigurationForm
from server.catalog.models import Instrument

from pprint import pformat
import logging


logger = logging.getLogger('sans.eq-sans')

instrument_name = "EQ-SANS"

class ConfigurationList(LoginRequiredMixin, ListView):
    '''
    List all configurations.
    '''
    template_name = 'sans/eq-sans/configuration_list.html'
    model = EQSANSConfiguration

class ConfigurationDetail(LoginRequiredMixin, DetailView):
    '''
    Detail of a configuration
    '''
    template_name = 'sans/eq-sans/configuration_detail.html'
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
    template_name = 'sans/eq-sans/configuration_form.html'
    form_class = ConfigurationForm
    
#     def get_initial(self):
#         # Get the initial dictionary from the superclass method
#         initial = super(ConfigurationCreate, self).get_initial()
#         # Copy the dictionary so we don't accidentally change a mutable dict
#         initial = initial.copy()
#         initial['user'] = self.request.user.pk
#         initial['instrument'] = get_object_or_404(Instrument, name=instrument_name)
#         return initial
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.instrument = get_object_or_404(Instrument, name=instrument_name)
        return CreateView.form_valid(self, form)

class ConfigurationUpdate(LoginRequiredMixin, UpdateView):
    '''
    Detail of a configuration
    '''
    template_name = 'sans/eq-sans/configuration_form.html'
    form_class = ConfigurationForm
    model = EQSANSConfiguration

#
#
#

class ReductionList(LoginRequiredMixin, ListView):
    '''
    List all Reduction.
    '''
    template_name = 'sans/eq-sans/reduction_list.html'
    model = EQSANSReduction

class ReductionDetail(LoginRequiredMixin, DetailView):
    '''
    Detail of a Reduction
    '''
    template_name = 'sans/eq-sans/reduction_detail.html'
    model = EQSANSReduction

class ReductionCreate(LoginRequiredMixin, CreateView):
    '''
    Detail of a configuration
    '''
    template_name = 'sans/eq-sans/reduction_form.html'
    model = EQSANSReduction
    fields = '__all__'