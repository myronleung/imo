# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-09 20:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imo_app', '0048_friendship_friend_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendship',
            name='friend_name',
            field=models.CharField(default='', max_length=200),
        ),
    ]
