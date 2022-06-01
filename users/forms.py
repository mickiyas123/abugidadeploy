""" A module for generating
    user registration form
"""
from django.forms import ModelForm, models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class CustomUserCreationForm(UserCreationForm):
    """ A class for generating user sign up form """
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']

        labels =  {
            'first_name': 'Name' 
        }
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class' : 'input'})



class ProfileForm(ModelForm):
    """ A class for genrating profile form """
    class Meta:
        model = Profile
        fields = ['name', 'username', 'email',
                  'bio', 'profile_pic',
                  'github_account', 'twitter_account', 'linkedin_account',
                  'personal_website']