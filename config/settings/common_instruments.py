"""

Dynamic configuration for instruments.

The model classes will be here.

"""


INSTRUMENT_MODULES = { 
    "BIOSANS" : { 
      "model_common" : "server.configuration.models.BioSANSCommon",
      "model_scan" : "server.configuration.models.BioSANSScan",
      "form_common" : "server.configuration.forms.BioSANSCommon",
      "form_scan" : "server.configuration.forms.BioSANSScan",
    }
}