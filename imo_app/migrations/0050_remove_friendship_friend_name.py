# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-09 21:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imo_app', '0049_auto_20160609_1645'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='friendship',
            name='friend_name',
        ),
    ]
