from django import forms
from django.contrib.auth.models import User
from quotes.models import Profile

from .models import Quotes

class DateInput(forms.DateInput):
    input_type = 'date'

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class QuoteForm(forms.ModelForm):

    class Meta:
        model = Quotes
        fields = ['quote_text', 'category_name']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'location', 'birth_date', 'profile_pic']
        widgets = {
            'birth_date': DateInput(),
        }