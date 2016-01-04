# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-04 15:23
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_auto_20160104_1023'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('configuration', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='USANSSANSCommon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ipts', models.CharField(max_length=16)),
                ('title', models.CharField(max_length=256)),
                ('label', models.CharField(choices=[('0', ''), ('1', 'Template'), ('2', 'TODO 1'), ('3', 'TODO 2')], default='0', max_length=1)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('empty_transmission_run', models.CharField(max_length=256)),
                ('dark_current_run', models.CharField(max_length=256)),
                ('flood_field_run', models.CharField(max_length=256)),
                ('beam_center_run', models.CharField(max_length=256)),
                ('instrument', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.Instrument')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='USANSSANSScan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('data_run', models.CharField(max_length=256)),
                ('background_run', models.CharField(max_length=256)),
                ('transmission_run', models.CharField(max_length=256)),
                ('configuration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configuration.USANSSANSCommon')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]