# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-06 03:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imo_app', '0035_auto_20160605_1911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='total_votes',
            field=models.IntegerField(default=0.5),
        ),
    ]
