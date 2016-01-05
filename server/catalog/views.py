# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.contrib import messages
from django.views.generic import View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from pprint import pformat
import logging

from .icat.facade import Catalog
from .permissions import user_has_permission_to_see_this_ipts
from .models import Instrument
from server.users.models import UserProfile

logger = logging.getLogger('catalog')


class InstrumentMixin(object):
    '''
    Context enhancer
    mixin that sets the shared context variables:
    instrument
    '''
    def get_context_data(self, **kwargs):
        #context = super().get_context_data(**kwargs)
        context = super(InstrumentMixin, self).get_context_data(**kwargs)
        context["instrument"] = kwargs.get('instrument', None)
        context["ipts"] = kwargs.get('ipts', None)
        return context

class Instruments(LoginRequiredMixin,View):
    '''
    List of visible instruments in the database
    '''
    def get(self, request):
        instruments = Instrument.objects.visible_instruments()
        logger.debug(pformat(instruments.values()))
        return render(request, 'catalog/list_instruments.html',
                      {'instruments' : instruments})
    

class IPTSs(LoginRequiredMixin,InstrumentMixin, TemplateView):
    '''
    List of IPTSs for a given instrument
    '''
    
    template_name = 'catalog/list_iptss.html'
 
    def get_context_data(self, **kwargs):
        icat = Catalog(self.request)
        iptss = icat.get_experiments_meta(kwargs['instrument'])
        context = super(IPTSs, self).get_context_data(**kwargs)
        context['iptss'] = iptss
        return context
    

class Runs(LoginRequiredMixin,InstrumentMixin,TemplateView):
    '''
    List of runs for a given instrument
    '''
    
    template_name = 'catalog/list_runs.html'
    
    def get_context_data(self, **kwargs):
        instrument = kwargs['instrument']
        ipts = kwargs['ipts']
        if user_has_permission_to_see_this_ipts(self.request.user,instrument,ipts):
            icat = Catalog(self.request)
            runs = icat.get_runs_all(instrument, ipts)
        else:
            # from django.http import HttpResponseForbidden
            # return HttpResponseForbidden()
            messages.error(self.request, "You do not have permission to see the details of the %s from %s."%(ipts,instrument))
            runs = []
        context = super(Runs, self).get_context_data(**kwargs)
        context['runs'] = runs
        return context




            
    
            