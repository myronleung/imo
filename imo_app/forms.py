from django import forms
from django.contrib.auth.models import User
from .models import Question, UserProfile, Feedback


class RegistrationForm(forms.Form):
    first_name = forms.CharField(label='First Name:', max_length=200)
    last_name = forms.CharField(label='Last Name:', max_length=200)
    email = forms.EmailField(label='Email:')
    password = forms.CharField(label='Password:', widget=forms.PasswordInput())

class VerifyForm(forms.Form):
    activation_key = forms.CharField(label='activation_key:', max_length=200)

class LoginForm(forms.Form):
    username = forms.CharField(label='Username:', max_length=200)
    password = forms.CharField(label='Password:', widget=forms.PasswordInput())

class NewEntryForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = [
            "question_text",
            "description",
            "choice1",
            "image1",
            "choice2",
            "image2",
            "choice3",
            "image3"
        ]

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            "gender",
            "picture",
            "birthday",
            "about",
            "motto",
        ]

class VoteForm(forms.Form):
    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('choices')
        super(VoteForm,self).__init__(*args,**kwargs)
        choice = forms.ChoiceField(choices=choices, widget=forms.RadioSelect())

class CommentForm(forms.Form):
    comment_text = forms.CharField(label='Comment: ', max_length = 1000)

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = [
            "topic",
            "feedback",
            "screenshot"
        ]
