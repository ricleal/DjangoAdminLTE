# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-25 20:04
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sans', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='eqsansconfiguration',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', related_query_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]
