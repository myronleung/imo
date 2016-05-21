from django import forms
from django.contrib.auth.models import User


class RegistrationForm(forms.Form):
    first_name = forms.CharField(label='First Name:', max_length=200)
    last_name = forms.CharField(label='Last Name:', max_length=200)
    email = forms.EmailField(label='Email:')
    password = forms.CharField(label='Password:', widget=forms.PasswordInput())

class LoginForm(forms.Form):
    username = forms.CharField(label='Username:', max_length=200)
    password = forms.CharField(label='Password:', widget=forms.PasswordInput())

class NewEntryForm(forms.Form):
    question_text = forms.CharField(label='Question: ', max_length = 200)
    description = forms.CharField(widget=forms.Textarea)
    choice1 = forms.CharField(label='Choice 1: ', max_length = 200)
    choice2 = forms.CharField(label='Choice 2: ', max_length = 200)

class ChangeEntryForm(forms.Form):
    question_text = forms.CharField(label='Question: ', max_length = 200)
    description = forms.CharField(widget=forms.Textarea)
    choice1 = forms.CharField(label='Choice 1: ', max_length = 200)
    choice2 = forms.CharField(label='Choice 2: ', max_length = 200)

class VoteForm(forms.Form):
    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('choices')
        super(VoteForm,self).__init__(*args,**kwargs)
        choice = forms.ChoiceField(choices=choices, widget=forms.RadioSelect())

class CommentForm(forms.Form):
    comment_text = forms.CharField(label='Comment: ', max_length = 1000)
