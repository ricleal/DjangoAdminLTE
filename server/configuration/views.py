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

# Create your views here.
#@login_required
class ConfigurationList(LoginRequiredMixin,ListView):
    template_name = 'configuration/configuration_list.html'
    # def get(self, request, *args, **kwargs):
    #     instrument = request.session['instrument']
    #     self.model = import_string(settings.INSTRUMENT_MODULES[instrument]["model_common"])
    model = import_string(settings.INSTRUMENT_MODULES['BIOSANS']["model_common"])
