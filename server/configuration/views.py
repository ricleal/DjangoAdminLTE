from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings

import logging

logger = logging.getLogger('configuration')

def import_string(import_name):
    '''
    Import class from String
    '''
    try:
        if '.' in import_name:
            module, obj = import_name.rsplit('.', 1)
            return getattr(__import__(module, None, None, [obj]), obj)
        else:
            return __import__(import_name)
    except (ImportError, AttributeError), e:
        print e


class SetModelMixin(object):
    def dispatch(self, request, *args, **kwargs):
        instrument = self.request.user.profile.instrument.name
        SetModelMixin.model = import_string(settings.INSTRUMENT_MODULES[instrument]["model_common"])
        return super(SetModelMixin, self).dispatch(request, *args, **kwargs)

class ConfigurationList(LoginRequiredMixin,SetModelMixin,ListView):
    '''
    List all configurations.
    '''
    template_name = 'configuration/configuration_list.html'


class ConfigurationDetail(LoginRequiredMixin,SetModelMixin,DetailView):
    '''
    Detail of a configuration
    '''
    template_name = 'configuration/configuration_detail.html'
    
