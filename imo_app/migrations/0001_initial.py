# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-14 19:45
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to=b'')),
                ('choice_text', models.CharField(max_length=200)),
                ('votes', models.IntegerField(default=0)),
                ('percentage', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_text', models.CharField(default='', max_length=1000)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
            ],
            options={
                'ordering': ['-pub_date'],
            },
        ),
        migrations.CreateModel(
            name='Friendship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default='', max_length=50)),
                ('relation_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_name', models.CharField(default='', max_length=200)),
                ('question_text', models.CharField(max_length=200)),
                ('description', models.TextField(default='')),
                ('category', models.CharField(default='', max_length=50)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('choice1', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('image1', models.ImageField(blank=True, null=True, upload_to=b'')),
                ('choice2', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('image2', models.ImageField(blank=True, null=True, upload_to=b'')),
                ('choice3', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('image3', models.ImageField(blank=True, null=True, upload_to=b'')),
                ('total_votes', models.IntegerField(default=1)),
                ('inappropriate', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['-pub_date'],
            },
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=200)),
                ('gender', models.CharField(blank=True, default='', max_length=15)),
                ('picture', models.ImageField(blank=True, default='', null=True, upload_to=b'')),
                ('birthday', models.DateField(blank=True, null=True)),
                ('about', models.TextField(blank=True, default='', null=True)),
                ('motto', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('total_friends', models.IntegerField(default=0)),
                ('inappropriate', models.IntegerField(default=0)),
                ('sponsor', models.BooleanField(default=False)),
                ('verification', models.BooleanField(default=False)),
                ('activation_key', models.CharField(default='', max_length=100)),
                ('terms_of_service', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Voted',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='imo_app.Question')),
                ('voter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='imo_app.UserProfile')),
            ],
        ),
        migrations.AddField(
            model_name='reply',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='imo_app.UserProfile'),
        ),
        migrations.AddField(
            model_name='reply',
            name='reply_text',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='imo_app.Comment'),
        ),
        migrations.AddField(
            model_name='question',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='imo_app.UserProfile'),
        ),
        migrations.AddField(
            model_name='friendship',
            name='friend',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend_set', to='imo_app.UserProfile'),
        ),
        migrations.AddField(
            model_name='friendship',
            name='requester',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friendship_creator_set', to='imo_app.UserProfile'),
        ),
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='imo_app.UserProfile'),
        ),
        migrations.AddField(
            model_name='comment',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='imo_app.Question'),
        ),
        migrations.AddField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='imo_app.Question'),
        ),
    ]
