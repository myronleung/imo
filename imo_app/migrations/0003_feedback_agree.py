# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-15 19:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imo_app', '0002_auto_20160615_1501'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='agree',
            field=models.IntegerField(default=0),
        ),
    ]
