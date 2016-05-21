from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)

    def __str__(self):
        return self.user.username

class Question(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    description = models.TextField(default = '')
    pub_date = models.DateTimeField('date published')

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

class Comment(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=1000, default = '')
    pub_date = models.DateTimeField('date published')

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.comments_text

class Reply(models.Model):
    reply_text = models.ForeignKey(Comment, on_delete=models.CASCADE)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.reply_text

class Voted(models.Model):
    voter = models.ForeignKey(UserProfile)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
