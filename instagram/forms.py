from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Image,Profile 

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254)
    fullname=forms.CharField(max_length=254)

    class Meta:
        model = User
        fields = ('username', 'fullname', 'email', 'password1','password2')
        
        
class UploadImageModelForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('image','name', 'caption')


class UpdateUserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'profile_picture')
