# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.db import models


class Facility(models.Model):
    '''
    Facility
    '''
    # Attributes
    name = models.CharField(max_length=128, unique=True)
    short_name = models.CharField(max_length=56, unique=True)

    # We can have instruments but they will be invisible in the web page
    visible = models.BooleanField(default=True, help_text = _("If it will be visible on the main catalog page"),)

    def __unicode__(self):
        return  self.short_name

    # Meta
    class Meta:
        verbose_name = _("Facility")
        verbose_name_plural = _("Facilities")
        ordering = ["short_name"]

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
    type = models.CharField(max_length=32, blank=True,  help_text = _("Type of instrument: SANS, TOF, etc.."),)
    description = models.CharField(max_length=256,
                                   blank=True,
                                   verbose_name = _("description"),
                                   help_text = _("Instrument description (optional)" ),
                                   )
    icat_name = models.CharField(max_length=32, blank=True)
    ldap_name = models.CharField(max_length=32, blank=True)
    drive_name = models.CharField(max_length=32, blank=True)
    # We can have instruments but they will be invisible in the web page
    visible = models.BooleanField(default=True, help_text = _("If it will be visible on the main catalog page"),)
    reduction_available = models.BooleanField(default=False, help_text = _("If there is web reduction available for this instrument"),)

    facility = models.ForeignKey(Facility, on_delete=models.CASCADE,
                                   related_name="facilities",
                                   related_query_name="facility",)  # , blank=True, null=True)

    def __unicode__(self):
        return  "%s (%s)"%(self.name, self.facility.short_name)

    # Manager
    objects = InstrumentManager()

    # Meta
    class Meta:
        verbose_name = _("Instrument")
        verbose_name_plural = _("Instruments")
        ordering = ["name"]
