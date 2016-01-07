from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .eqsans.models import EQSANSConfiguration, EQSANSEntry, EQSANSReduction 
                    
# Register your models here.
admin.site.register(EQSANSConfiguration)
admin.site.register(EQSANSEntry)
admin.site.register(EQSANSReduction)
