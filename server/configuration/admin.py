from django.contrib import admin
from .models import BioSANSCommon, BioSANSScan, \
                    USANSSANSCommon, USANSSANSScan
                    
# Register your models here.
admin.site.register(BioSANSCommon)
admin.site.register(BioSANSScan)

admin.site.register(USANSSANSCommon)
admin.site.register(USANSSANSScan)
