from __future__ import unicode_literals

from django.db.models import Q

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=200, default='')
    gender = models.CharField(default='', blank=True, max_length=15)
    picture = models.ImageField(blank=True, null=True, default='')
    birthday = models.DateField(blank=True, null=True)
    about = models.TextField(null = True, blank = True, default='')
    motto = models.CharField(max_length=200, null = True, blank=True, default='')
    total_friends = models.IntegerField(default=0)
    inappropriate = models.IntegerField(default=0)
    sponsor = models.BooleanField(default=False)
    verification = models.BooleanField(default=False)
    activation_key = models.CharField(max_length=100, default='')
    terms_of_service = models.BooleanField(default=False)   

    def __str__(self):
        return self.user.username

    def get_friends(self):
        user = self.user
        return Friendship.objects.filter(Q(requestor=user)|Q(friend=user))

class Question(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    author_name = models.CharField(max_length=200, default='')
    question_text = models.CharField(max_length=200)
    description = models.TextField(default = '')
    category = models.CharField(max_length=50, default='')
    pub_date = models.DateTimeField('date published')
    choice1 = models.CharField(null=True, blank=True, default = '', max_length = 200)
    image1 = models.ImageField(null=True, blank=True)
    choice2 = models.CharField(null=True, blank=True, default = '', max_length = 200)
    image2 = models.ImageField(null=True, blank=True)
    choice3 = models.CharField(null=True, blank=True, default = '', max_length = 200)
    image3 = models.ImageField(null=True, blank=True)
    total_votes = models.IntegerField(default = 1)
    inappropriate = models.IntegerField(default=0)


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

class Friendship(models.Model):
    requester = models.ForeignKey(UserProfile, related_name="friendship_creator_set")
    friend = models.ForeignKey(UserProfile, related_name="friend_set")
    status = models.CharField(max_length=50, default='')
    relation_date = models.DateTimeField(auto_now_add=True, editable=False)
