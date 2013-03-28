from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from userwinparf.models import Userwinparf

class RegistrationForm(ModelForm):
        ''' This is the form to register as a userwinparf. '''
        username        = forms.CharField(label=(u'User Name'))
        email           = forms.EmailField(label=(u'Email Address'))
        password        = forms.CharField(label=(u'Password'), widget=forms.PasswordInput(render_value=False))
        password1       = forms.CharField(label=(u'Verify Password'), widget=forms.PasswordInput(render_value=False))
        status          = forms.CharField(required=False)

        class Meta:
                model = Userwinparf
                exclude = ('user',)

        def clean_username(self):
                ''' Check if the username already exists or not.'''
                username = self.cleaned_data['username']
                try:
                        User.objects.get(username=username)
                except User.DoesNotExist:
                        return username
                raise forms.ValidationError("That username is already taken, please select another.")

        def clean_password1(self):
                ''' Check that the two passwords match'''
                if self.cleaned_data['password'] != self.cleaned_data['password1']:
                        raise forms.ValidationError("The passwords did not match.  Please try again.")
                return self.cleaned_data

class LoginForm(forms.Form):
        ''' This is the form to log into the website. '''
        username        = forms.CharField(label=(u'User Name'))
        password        = forms.CharField(label=(u'Password'), widget=forms.PasswordInput(render_value=False))
                

