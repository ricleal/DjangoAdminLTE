from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
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
    return render_to_response('catalog/list_instruments.html',
                              {'instruments' : instruments},
                              context_instance=RequestContext(request))

@login_required
def list_iptss(request, instrument):
    dumper = icat.DjangoDumper(request)
    iCat = icat.ICat(dumper)
    iptss = iCat.get_experiments_meta(instrument)
    return render_to_response('catalog/list_iptss.html',
                              {'iptss' : iptss},
                              context_instance=RequestContext(request))
