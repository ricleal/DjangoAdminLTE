from django.shortcuts import render
from django.contrib.auth.decorators import login_required

import logging

from . import icat

logger = logging.getLogger('catalog')

@login_required
def list_instruments(request):
    """

    """
    dumper = icat.DjangoDumper(request)
    iCat = icat.ICat(dumper)
    instruments = iCat.get_instruments()
    return render(request, 'catalog/list_instruments.html',
        {'instruments' : instruments})

@login_required
def list_iptss(request, instrument):
    dumper = icat.DjangoDumper(request)
    iCat = icat.ICat(dumper)
    iptss = iCat.get_experiments_meta(instrument)
    request.session['instrument'] = instrument
    return render(request, 'catalog/list_iptss.html', {'iptss' : iptss})
