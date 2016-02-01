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
    
    mask_file = models.CharField(max_length=256, blank=True, help_text="File path")
    dark_current_file = models.CharField(max_length=256, blank=True, help_text="File path")
    sensitivity_file = models.CharField(max_length=256, blank=True, help_text="File path")
    
    sensitivity_min = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.4)
    sensitivity_max = models.DecimalField(
        max_digits=10, decimal_places=2, default=2.0)
    direct_beam_file = models.CharField(max_length=256, blank=True, null=True,)
    

    @models.permalink
    def get_absolute_url(self):
        return ('sans:eq-sans_configuration_detail', [self.pk])

class EQSANSReduction(Reduction):
    configuration = models.ForeignKey(EQSANSConfiguration, on_delete=models.CASCADE,
                                      related_name="reductions",
                                      related_query_name="reduction",
                                      blank=True, null=True,)
    
    @models.permalink
    def get_absolute_url(self):
        return ('sans:eq-sans_reduction_detail', [self.pk])


class EQSANSEntry(Entry):
    # We can not have ForeignKey for abstract models. It has to be here!!
    reduction = models.ForeignKey(EQSANSReduction,
                                      on_delete=models.CASCADE,
                                      related_name="entries",
                                      related_query_name="entry",)
    
    def __unicode__(self):
        return "Entry: %s :: Reduction: %s" % (self.save_name, self.reduction.title)
