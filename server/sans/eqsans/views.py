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

class ConfigurationList(LoginRequiredMixin, ListView):
    '''
    List all configurations.
    '''
    template_name = 'sans/eq-sans/configuration_list.html'
    #model = EQSANSConfiguration

    def get_queryset(self):
        ConfigurationList.queryset = EQSANSConfiguration.objects.filter(user = self.request.user)
        return ListView.get_queryset(self)

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


#######################################################################
#
# Reduction
#
#######################################################################

class ReductionList(LoginRequiredMixin, ListView):
    '''
    List all Reduction.
    '''
    template_name = 'sans/eq-sans/reduction_list.html'
    #model = EQSANSReduction
    def get_queryset(self):
        ReductionList.queryset = EQSANSReduction.objects.filter(configuration__user = self.request.user)
        return ListView.get_queryset(self)


class EntryMixin(object):

    def get_context_data(self, **kwargs):
        logger.debug(pformat(kwargs))
        logger.debug(pformat(self.kwargs))
        context = super(EntryMixin, self).get_context_data(**kwargs)
        context["entry_headers"] = EQSANSEntry.get_field_titled_names()
        context["entry_names"] = EQSANSEntry.get_field_names()
        return context

    def form_valid(self, form):
        '''
        Stores the handsontable in a variable
        '''
        logger.debug(self.request.POST["entries_hidden"]);
        self.handsontable = json.loads(self.request.POST["entries_hidden"])
        return super(EntryMixin, self).form_valid(form)


class ReductionDetail(LoginRequiredMixin, EntryMixin, DetailView):
    '''
    Detail of a Reduction

    A Reduction is a title and a set of entries.
    The entries are an hidden field : id="entries_hidden"
    Which are an Handsontable

    '''
    template_name = 'sans/eq-sans/reduction_detail.html'
    model = EQSANSReduction

    #TODO: Get query set by user


class ReductionCreate(LoginRequiredMixin,EntryMixin, CreateView):
    '''
    Detail of a Reduction
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

class ReductionUpdate(LoginRequiredMixin,EntryMixin, UpdateView):
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
