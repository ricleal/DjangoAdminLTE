from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, RedirectView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.http import Http404
from django.contrib import messages
from django.core.serializers.json import DjangoJSONEncoder
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType

from .models import EQSANSConfiguration, EQSANSReduction, EQSANSEntry
from .forms import ConfigurationForm
from server.catalog.models import Instrument
from server.util.script import build_script

from pprint import pformat
import logging
import json
import os

logger = logging.getLogger('sans.eq-sans')

instrument_name = "EQ-SANS"
script_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),"scripts","template.py")

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


class ConfigurationDelete(LoginRequiredMixin, DeleteView):
    
    model = EQSANSConfiguration
    success_url = reverse_lazy('sans:eq-sans_configuration_list')

    def get_object(self, queryset=None):
        """
        Hook to ensure object is owned by request.user.
        """
        obj = super(ConfigurationDelete, self).get_object()
        if not obj.user  == self.request.user:
            raise Http404
        logger.debug("Deleting %s"%obj)
        return obj


class ConfigurationClone(LoginRequiredMixin, ConfigurationMixin, DetailView):
    '''
    
    '''
    template_name = 'sans/eq-sans/configuration_detail.html'
    #model = EQSANSConfiguration

    def get_object(self):
        obj = EQSANSConfiguration.objects.clone(self.kwargs['pk'])
        self.kwargs['pk'] = obj.pk
        messages.success(self.request, 'Configuration %s cloned. New id = %s'%(obj, obj.pk))
        return obj

class ConfigurationAssign(LoginRequiredMixin, ConfigurationMixin, DetailView):
    '''
    
    '''
    template_name = 'sans/eq-sans/configuration_detail.html'
    model = EQSANSConfiguration
    
    def get(self, request, *args, **kwargs):
        obj = EQSANSConfiguration.objects.clone_and_assign_new_user(kwargs['pk'],kwargs['uid'])
        messages.success(request, "Configuration '%s' assigned to %s. New id = %s"%(obj, obj.user, obj.pk))
        return super(ConfigurationAssign, self).get(request, *args, **kwargs)
    
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
    Edit a Reduction
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

class ReductionDelete(LoginRequiredMixin, DeleteView):
    
    model = EQSANSReduction
    success_url = reverse_lazy('sans:eq-sans_reduction_list')

    def get_object(self, queryset=None):
        """
        Hook to ensure object is owned by request.user.
        """
        
        obj = super(ReductionDelete, self).get_object()
        if not obj.configuration.user  == self.request.user:
            raise Http404
        logger.debug("Deleting %s"%obj)
        return obj

   
# class ReductionClone(LoginRequiredMixin, ReductionMixin, DetailView):
#     '''
#     Configuration clone
#     '''
#     template_name = 'sans/eq-sans/reduction_detail.html'
#     
#     def get_object(self):
#         '''
#         Clones a reduction and related entries.
#         '''
#         obj = EQSANSReduction.objects.clone(self.kwargs['pk'])
#         self.kwargs['pk'] = obj.pk
#         messages.success(self.request, "Reduction '%s' cloned. New id = %s"%(obj, obj.pk))
#         return obj

class ReductionClone(LoginRequiredMixin, ReductionMixin, RedirectView):
    '''
    Configuration clone using redirect
    '''
    permanent = True
    query_string = False
    pattern_name = 'sans:eq-sans_reduction_update'

    def get_redirect_url(self, *args, **kwargs):
        obj = EQSANSReduction.objects.clone(self.kwargs['pk'])
        messages.success(self.request, "Reduction '%s' cloned. New id = %s"%(obj, obj.pk))
        self.url = reverse(self.pattern_name, kwargs={'pk': obj.pk})
        return super(ReductionClone, self).get_redirect_url(*args, **kwargs)


class ReductionScript(LoginRequiredMixin, ReductionMixin, RedirectView):
    '''
    Generates the script, puts in in the session and redirects to job form
    '''
    permanent = True
    query_string = False
    # Pattern is not working!
    pattern_name = 'jobs:job_create'
    url = '/jobs/create'
    
    def get_redirect_url(self, *args, **kwargs):
        logger.debug("Redirecting to %s...."%reverse(self.pattern_name))
        obj_json = EQSANSReduction.objects.to_json(kwargs['pk'])
        self.request.session['script'] = build_script(script_file, obj_json)
        self.request.session['content_type'] = ContentType.objects.get(app_label="sans", model="eqsansreduction")
        self.request.session['object_id'] =  kwargs['pk']
        return super(ReductionScript, self).get_redirect_url(*args, **kwargs)


    
    