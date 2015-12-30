from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, FormView

from django.conf import settings

import importlib
from .models import BioSANSCommon

# Create your views here.
class ConfigurationList(ListView):
    model = importlib.import_module(settings.INSTRUMENT_MODULES["BIOSANS"]["model_common"])

