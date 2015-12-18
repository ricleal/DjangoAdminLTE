from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from . import icat

from pprint import pprint

def list_instruments(request):
    """

    """
    dumper = icat.DjangoDumper(request)
    iCat = icat.ICat(dumper)
    instruments = iCat.get_instruments()
    return render_to_response('catalog/list_instruments.html',
                              {'instruments' : instruments['instrument']},
                              context_instance=RequestContext(request))

def list_iptss(request, instrument):
    dumper = icat.DjangoDumper(request)
    iCat = icat.ICat(dumper)
    iptss = iCat.get_experiments_meta(instrument)
    return render_to_response('catalog/list_iptss.html',
                              {'iptss' : iptss['proposal']},
                              context_instance=RequestContext(request))
