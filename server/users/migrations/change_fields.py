# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


class Migration(migrations.Migration):
    '''
    Change original fields for User model
    
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
        
    '''
    
    def __init__(self, name, app_label):
        return super(Migration, self).__init__(name, app_label='auth')

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth','0001_initial'),
    ]
    operations = [
        migrations.AlterField(
            model_name='User',
            name='first_name',
            field=models.CharField(_('first name'), max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='User',
            name='last_name',
            field=models.CharField(_('last name'), max_length=100, blank=True),
        ),
                  
    ]