# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings

import logging
import json
import os.path

from .icat.facade import Catalog
from .permissions import user_has_permission_to_see_this_ipts
from .models import Instrument

logger = logging.getLogger('catalog')

@login_required
def list_instruments(request):
    """
    Get instrument list + descriptions from the database
    """
    instruments = Instrument.objects.visible_instruments()
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



            
    
            