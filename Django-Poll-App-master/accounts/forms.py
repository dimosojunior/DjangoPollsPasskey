from django import forms
from django.contrib.auth.models import User
from django import forms
from polls.models import *

from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,PasswordChangeForm, UserChangeForm
from django.contrib.auth import authenticate

from django.conf import settings


# class UserRegistrationForm(forms.Form):
#     username = forms.CharField(label='Username', max_length=100, min_length=5,
#                                widget=forms.TextInput(attrs={'class': 'form-control'}))
#     email = forms.EmailField(label='Email', max_length=20, min_length=5,
#                              widget=forms.EmailInput(attrs={'class': 'form-control'}))
#     password1 = forms.CharField(label='Password', max_length=50, min_length=5,
#                                 widget=forms.PasswordInput(attrs={'class': 'form-control'}))
#     password2 = forms.CharField(label='Confirm Password',
#                                 max_length=50, min_length=5,
#                                 widget=forms.PasswordInput(attrs={'class': 'form-control'}))




class UserRegistrationForm(UserCreationForm):
	username = forms.IntegerField(
		required=True,
		#label=True,
		widget=forms.NumberInput(attrs={'class' :'input'})

	)
	email = forms.EmailField(
		required=True,
		widget=forms.EmailInput(attrs={'class': 'input'})
	)

	password1 = forms.CharField(
		required=True,
		#label=True,
		widget=forms.PasswordInput(attrs={'class' :'input'})

	)

	password2 = forms.CharField(
		required=True,
		#label=True,
		widget=forms.PasswordInput(attrs={'class' :'input'})

	)

	Course = forms.ModelChoiceField(
		queryset=Courses.objects.all(),
		required=True,
		label=False,
		widget=forms.Select(attrs={'class': 'input'})
	)

	Year = forms.ModelChoiceField(
		queryset=Years.objects.all(),
		required=True,
		widget=forms.Select(attrs={'class': 'input'})
	)

	College = forms.ModelChoiceField(
		queryset=Colleges.objects.all(),
		required=True,
		widget=forms.Select(attrs={'class': 'input'})
	)

	Location = forms.ModelChoiceField(
		queryset=Location.objects.all(),
		required=True,
		widget=forms.Select(attrs={'class': 'input'})
	)
    
    
    
	class Meta:
	    model = MyUser
	    fields = (
	    "email",
	    "username",
	    "password1",
	    "password2",
	    "Course",
	    "Year",
	    "Location",
	    "College"
	    

	    
         )
	def clean_email(self):
	    email = self.cleaned_data['email'].lower()
	    try:
	        myuser = MyUser.objects.get(email=email)
	    except Exception as e:
	        return email
	    raise forms.ValidationError(f"Email {email} is already exist.")

	def clean_username(self):
	    username = self.cleaned_data['username']
	    try:
	        myuser = MyUser.objects.get(username=username)
	    except Exception as e:
	        return username
	    raise forms.ValidationError(f"username {username} is already exist.")

