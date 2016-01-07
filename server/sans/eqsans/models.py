from __future__ import unicode_literals

from django.db import models

from ..models import Configuration, Reduction, Entry

#
# EQSANS
#


class EQSANSConfiguration(Configuration):
    absolute_scale_factor = models.DecimalField(
        max_digits=10, decimal_places=2, default=1.0)
    sample_thickness = models.DecimalField(
        max_digits=10, decimal_places=2, default=1.0)
    sample_aperture_diameter = models.DecimalField(
        max_digits=10, decimal_places=2, default=10.0)
    sensitivity_run = models.CharField(max_length=256, blank=True, null=True,)
    sensitivity_min = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.4)
    sensitivity_max = models.DecimalField(
        max_digits=10, decimal_places=2, default=2.0)
    direct_beam_run = models.CharField(max_length=256, blank=True, null=True,)
    mask_run = models.CharField(max_length=256, blank=True, null=True,)

    @models.permalink
    def get_absolute_url(self):
        return ('sans:eqsans_configuration_list', [self.pk])

class EQSANSReduction(Reduction):
    configuration = models.ForeignKey(EQSANSConfiguration, on_delete=models.CASCADE,
                                      related_name="reduction",
                                      related_query_name="reduction",)


class EQSANSEntry(Entry):
    # We can not have ForeignKey for abstract models. It has to be here!!
    configuration = models.ForeignKey(EQSANSReduction,
                                      on_delete=models.CASCADE,
                                      related_name="entry",
                                      related_query_name="entry",)
