from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class createUser(UserCreationForm):
    password2 = None
    
    class Meta:
        model = User
        fields = ('email','username')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Email is taken")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("Username is taken")
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        return password