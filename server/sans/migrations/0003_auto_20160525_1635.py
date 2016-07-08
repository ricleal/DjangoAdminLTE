# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-25 20:35
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0001_initial'),
        ('sans', '0002_eqsansconfiguration_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='BIOSANSConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=256)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('absolute_scale_factor', models.DecimalField(decimal_places=2, default=1.0, max_digits=10)),
                ('sample_thickness', models.DecimalField(decimal_places=2, default=1.0, max_digits=10)),
                ('sample_aperture_diameter', models.DecimalField(decimal_places=2, default=10.0, max_digits=10)),
                ('direct_beam_file', models.CharField(blank=True, help_text='File path', max_length=256)),
                ('mask_file', models.CharField(blank=True, help_text='File path', max_length=256)),
                ('dark_current_file', models.CharField(blank=True, help_text='File path', max_length=256)),
                ('sensitivity_file', models.CharField(blank=True, help_text='File path', max_length=256)),
                ('sensitivity_min', models.DecimalField(decimal_places=2, default=0.4, max_digits=10)),
                ('sensitivity_max', models.DecimalField(decimal_places=2, default=2.0, max_digits=10)),
                ('instrument', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='biosansconfiguration_instruments', related_query_name='%(class)s_instrument', to='catalog.Instrument')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='biosansconfiguration_users', related_query_name='%(class)s_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BIOSANSEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sample_scattering', models.CharField(max_length=256)),
                ('sample_transmission', models.CharField(max_length=256)),
                ('background_scattering', models.CharField(max_length=256)),
                ('background_transmission', models.CharField(max_length=256)),
                ('save_name', models.CharField(blank=True, max_length=256)),
            ],
            options={
                'ordering': ['id'],
                'abstract': False,
                'verbose_name_plural': 'Entries',
            },
        ),
        migrations.CreateModel(
            name='BIOSANSReduction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=256)),
                ('ipts', models.CharField(blank=True, max_length=16, verbose_name='Integrated Proposal Tracking System (IPTS)')),
                ('empty_beam', models.CharField(max_length=256)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('configuration', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reductions', related_query_name='reduction', to='sans.BIOSANSConfiguration')),
            ],
            options={
                'ordering': ['id'],
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='eqsansconfiguration',
            name='instrument',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='eqsansconfiguration_instruments', related_query_name='%(class)s_instrument', to='catalog.Instrument'),
        ),
        migrations.AlterField(
            model_name='eqsansconfiguration',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='eqsansconfiguration_users', related_query_name='%(class)s_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='biosansentry',
            name='reduction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entries', related_query_name='entry', to='sans.BIOSANSReduction'),
        ),
    ]