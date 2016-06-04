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
    choice1 = models.CharField(null=True, blank=True, default = '', max_length = 200)
    image1 = models.ImageField(null=True, blank=True)
    choice2 = models.CharField(null=True, blank=True, default = '', max_length = 200)
    image2 = models.ImageField(null=True, blank=True)
    choice3 = models.CharField(null=True, blank=True, default = '', max_length = 200)
    image3 = models.ImageField(null=True, blank=True)
    total_votes = models.FloatField(default = 0.5)

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.question_text

    def get_absolute_url(self):
        return reverse("detail", kwargs={"id": self.id})
        #return "/posts/%s/" %(self.id)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    percentage = models.FloatField(default=0)

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
