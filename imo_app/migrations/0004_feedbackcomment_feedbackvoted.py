# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-15 19:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('imo_app', '0003_feedback_agree'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeedbackComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_text', models.CharField(default='', max_length=1000)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='imo_app.UserProfile')),
                ('feedback', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='imo_app.Feedback')),
            ],
            options={
                'ordering': ['-pub_date'],
            },
        ),
        migrations.CreateModel(
            name='FeedbackVoted',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='imo_app.Feedback')),
                ('voter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='imo_app.UserProfile')),
            ],
        ),
    ]