from django.contrib import admin

from .models import Job, Transaction
                    
# Register your models here.
admin.site.register(Job)
admin.site.register(Transaction)
