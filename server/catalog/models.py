# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.db import models

class InstrumentManager(models.Manager):
    '''
    Queries go here!!
    '''
    
    use_for_related_fields = True

    def visible_instruments(self, **kwargs):
        return self.filter(visible="True", **kwargs)

class Instrument(models.Model):
    '''
    Intrument
    '''
    # Attributes
    beamline = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=32, unique=True)
    description = models.CharField(max_length=256,
                                   blank=True,
                                   verbose_name = _("description"),
                                   help_text = _("Instrument description (optional)" ),
                                   )
    # We can have instruments but they will be invisible in the web page
    visible = models.BooleanField(default=True)

    def __unicode__(self):
        return  _("%s :: %s.") %  (self.beamline, self.name)
    
    # Manager
    objects = InstrumentManager()
    
    # Meta
    class Meta:
        verbose_name = _("Instrument")
        verbose_name_plural = _("Instruments")
        ordering = ["id"]