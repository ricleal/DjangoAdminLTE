from django.shortcuts import render
from django.contrib.auth.decorators import login_required

import logging

from .icat.facade import Catalog

logger = logging.getLogger('catalog')

@login_required
def list_instruments(request):
    """

    """
    icat = Catalog(request)
    instruments = icat.get_instruments()
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
    icat = Catalog(request)
    runs = icat.get_runs_all(instrument, ipts)
    request.session['instrument'] = instrument
    request.session['ipts'] = ipts
    return render(request, 'catalog/list_runs.html', {'runs' : runs})
