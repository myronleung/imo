# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-07 00:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imo_app', '0041_userprofile_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='about',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='motto',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
    ]