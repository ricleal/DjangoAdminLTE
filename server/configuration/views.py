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

class ConfigurationList(LoginRequiredMixin,ListView):
    '''
    List all configurations.
    '''
    template_name = 'configuration/configuration_list.html'

    def get_queryset(self):
        instrument = self.kwargs['instrument']      
        self.request.session['instrument'] = instrument
        model = import_string(settings.INSTRUMENT_MODULES[instrument]["model_common"])
        return model.objects.filter(owner=self.request.user, instrument__name = instrument)


class ConfigurationDetail(LoginRequiredMixin,DetailView):
    template_name = 'configuration/configuration_detail.html'
    model = import_string(settings.INSTRUMENT_MODULES["USANS"]["model_common"])