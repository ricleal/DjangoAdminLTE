from __future__ import unicode_literals

from django.db import models

from ..models import Configuration, Scan

#
# BIOSANS
#
class BioSANSCommon(Configuration):
    empty_transmission_run = models.CharField(max_length=256, blank=True, null=True,)
    flood_field_run = models.CharField(max_length=256, blank=True, null=True,)
    
class BioSANSScan(Scan):
    # We can not have ForeignKey for abstract models. It has to be here!!
    configuration = models.ForeignKey(BioSANSCommon,
                on_delete=models.CASCADE,
                related_name="scan",
                related_query_name="scan",)