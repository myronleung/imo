# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-15 19:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('imo_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(default='', max_length=200)),
                ('feedback', models.TextField(default='')),
                ('screenshot', models.ImageField(blank=True, null=True, upload_to='')),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
            ],
            options={
                'ordering': ['-pub_date'],
            },
        ),
        migrations.AlterField(
            model_name='choice',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
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
        migrations.AlterField(
            model_name='userprofile',
            name='picture',
            field=models.ImageField(blank=True, default='', null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='feedback',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='imo_app.UserProfile'),
        ),
    ]