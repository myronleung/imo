# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-01 19:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imo_app', '0016_auto_20160601_1528'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='choice3',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='image3',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
