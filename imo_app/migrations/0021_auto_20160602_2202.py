# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-03 02:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imo_app', '0020_auto_20160602_2202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='image1',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='question',
            name='image2',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='question',
            name='image3',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
