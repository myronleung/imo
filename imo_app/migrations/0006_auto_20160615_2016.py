# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-16 00:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imo_app', '0005_userprofile_join_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='total_votes',
            field=models.IntegerField(default=0),
        ),
    ]