# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-04 16:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imo_app', '0025_auto_20160604_1205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='choice3',
            field=models.CharField(default='', max_length=200),
        ),
    ]
