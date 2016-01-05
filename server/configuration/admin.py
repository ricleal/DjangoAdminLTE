from django.contrib import admin
from .models import BioSANSCommon, BioSANSScan, \
                    EQSANSCommon, EQSANSScan
                    
# Register your models here.
admin.site.register(BioSANSCommon)
admin.site.register(BioSANSScan)

admin.site.register(EQSANSCommon)
admin.site.register(EQSANSScan)
