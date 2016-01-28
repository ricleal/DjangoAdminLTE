from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

from .models import EQSANSConfiguration, EQSANSReduction, EQSANSEntry
from .forms import ConfigurationForm
from server.catalog.models import Instrument

from pprint import pformat
import logging
import json
from django.core.serializers.json import DjangoJSONEncoder

logger = logging.getLogger('sans.eq-sans')

instrument_name = "EQ-SANS"

class ConfigurationMixin(object):

    def get_queryset(self):
        '''
        Make sure the user only accesses its configurations
        '''
        return EQSANSConfiguration.objects.filter(user = self.request.user)

class ConfigurationList(LoginRequiredMixin, ConfigurationMixin, ListView):
    '''
    List all configurations.
    '''
    template_name = 'sans/eq-sans/configuration_list.html'
    #model = EQSANSConfiguration
    def get_queryset(self):
        return super(ConfigurationList, self).get_queryset()

class ConfigurationDetail(LoginRequiredMixin, ConfigurationMixin, DetailView):
    '''
    Detail of a configuration
    '''
    template_name = 'sans/eq-sans/configuration_detail.html'
    #model = EQSANSConfiguration

    def get_queryset(self):
        queryset = super(ConfigurationDetail, self).get_queryset()
        return queryset.filter(id = self.kwargs['pk'])

class ConfigurationCreate(LoginRequiredMixin, CreateView):
    '''
    Detail of a configuration
    '''
    template_name = 'sans/eq-sans/configuration_form.html'
    # Using form rather than model as we are hiding some fields!!
    form_class = ConfigurationForm

    def form_valid(self, form):
        """
        Sets initial values which are hidden in the form
        """
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


#######################################################################
#
# Reduction
#
#######################################################################

class ReductionMixin(object):
    '''
    Used in the template form to populate the redution spreadsheet
    '''

    def get_context_data(self, **kwargs):
        '''
        Populates the context with the titled case names and names as in the model
        '''
        context = super(ReductionMixin, self).get_context_data(**kwargs)
        context["entry_headers"] = EQSANSEntry.get_field_titled_names()
        context["entry_names"] = EQSANSEntry.get_field_names()
        return context

    def form_valid(self, form):
        '''
        Stores the handsontable in a variable
        '''
        #logger.debug(self.request.POST["entries_hidden"]);
        self.handsontable = json.loads(self.request.POST["entries_hidden"])
        return super(ReductionMixin, self).form_valid(form)

    def get_queryset(self):
        '''
        Get only reductions for this user: reduction.configuration.user
        '''
        return EQSANSReduction.objects.filter(configuration__user = self.request.user)

    def get_form(self, form_class=None):
        '''
        When creating a new form, this will make sure the user only sees it's own
        configurations
        '''
        form = super(ReductionMixin,self).get_form(form_class) #instantiate using parent
        form.fields['configuration'].queryset = EQSANSConfiguration.objects.filter(user = self.request.user)
        return form

class ReductionList(LoginRequiredMixin, ReductionMixin, ListView):
    '''
    List all Reduction.
    '''
    template_name = 'sans/eq-sans/reduction_list.html'
    # We wither use the model or the function get_queryset
    #model = EQSANSReduction
    def get_queryset(self):
        '''
        Get only reductions for this user: reduction.configuration.user
        '''
        return super(ReductionList, self).get_queryset()

class ReductionDetail(LoginRequiredMixin, ReductionMixin, DetailView):
    '''
    Detail of a Reduction

    A Reduction is a title and a set of entries.
    The entries are an hidden field : id="entries_hidden"
    Which are an Handsontable

    '''
    template_name = 'sans/eq-sans/reduction_detail.html'
    # either model or get_queryset
    #model = EQSANSReduction

    def get_queryset(self):
        '''
        Get only reductions for this user: reduction.configuration.user
        '''
        queryset = super(ReductionDetail, self).get_queryset()
        return queryset.filter(id = self.kwargs['pk'])

class ReductionCreate(LoginRequiredMixin,ReductionMixin, CreateView):
    '''
    Create a new entry!
    '''
    template_name = 'sans/eq-sans/reduction_form.html'
    model = EQSANSReduction
    fields = '__all__'
    handsontable = None

    def get_success_url(self):
        '''
        Called after the reduction was saved on the DB (after form_valid)
        It creates The entries for this reduction
        '''
        EQSANSEntry.objects.create_entries_from_handsontable(self.handsontable, reduction=self.object)
        return super(ReductionCreate, self).get_success_url()


class ReductionUpdate(LoginRequiredMixin,ReductionMixin, UpdateView):
    '''
    Detail of a Reduction
    '''
    template_name = 'sans/eq-sans/reduction_form.html'
    model = EQSANSReduction
    fields = '__all__'

    def get_context_data(self, **kwargs):
        '''
        Get all entries for this reduction and add them as json to the context
        This will poplulate the table
        '''
        context = super(ReductionUpdate, self).get_context_data(**kwargs)
        entries = EQSANSEntry.objects.filter(reduction__configuration__user = self.request.user,
                                                        reduction__id = self.kwargs['pk']).values()
        entries_json = json.dumps(list(entries), cls=DjangoJSONEncoder)
        context["entries"] = entries_json
        return context

    def get_success_url(self):
        '''
        Called after the reduction was saved on the DB (after form_valid)
        It deletes all Entries first and then create new ones with the table
        '''
        EQSANSEntry.objects.filter(reduction = self.object).delete()
        EQSANSEntry.objects.create_entries_from_handsontable(self.handsontable, reduction=self.object)
        return super(ReductionUpdate, self).get_success_url()
