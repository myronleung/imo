# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-03 04:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imo_app', '0022_auto_20160602_2331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='choice1',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
    ]