# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-05 21:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imo_app', '0033_auto_20160605_1719'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='author',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='birthday',
            field=models.DateTimeField(default=''),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='first_name',
            field=models.CharField(default='', max_length=120),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(default='', max_length=120),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='last_name',
            field=models.CharField(default='', max_length=120),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='picture',
            field=models.ImageField(blank=True, default='', null=True, upload_to=''),
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
