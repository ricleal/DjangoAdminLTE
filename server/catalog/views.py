from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

import logging
import json
import os.path

from .icat.facade import Catalog
from .permissions import user_has_permission_to_see_this_ipts

logger = logging.getLogger('catalog')

@login_required
def list_instruments(request):
    """

    """
    instrument = Instruments()
    instruments = instrument.get_instruments()
    return render(request, 'catalog/list_instruments.html',
        {'instruments' : instruments})

@login_required
def list_iptss(request, instrument):
    icat = Catalog(request)
    iptss = icat.get_experiments_meta(instrument)
    request.session['instrument'] = instrument
    return render(request, 'catalog/list_iptss.html', {'iptss' : iptss})

@login_required
def list_runs(request, instrument, ipts):
    if user_has_permission_to_see_this_ipts(request.user,instrument,ipts):
        icat = Catalog(request)
        runs = icat.get_runs_all(instrument, ipts)
    else:
        messages.error(request, "You do not have permission to see the details of the %s from %s."%(ipts,instrument))
        runs = []
    request.session['instrument'] = instrument
    request.session['ipts'] = ipts
    return render(request, 'catalog/list_runs.html', {'runs' : runs})


#### Aux FUNCTIONS
class Instruments():
    def __init__(self,filename="instruments.json"):
        self._filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), 
                                      filename)
        self._instruments = None
        logger.debug("Getting instruments from %s"%self._filename)
             
    def _parse_instruments(self):
        with open(self._filename) as data_file:    
            self._instruments = json.load(data_file)
    
    def get_instruments(self):
        if self._instruments is None:
            self._parse_instruments()
        return self._instruments
            
    
            