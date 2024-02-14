from django import forms
from django.contrib.auth.forms import UserCreationForm , UserChangeForm
from user.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='')  # Make email optional and remove help text
    profile_pic = forms.ImageField(required=False, help_text='')  # Make profile_pic optional and remove help text
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
        help_text='',  # Remove help text for password1
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput,
        strip=False,
        help_text='',  # Remove help text for password2
    )
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'profile_pic']
        help_texts = {
            'username': '',  # Removes help text for username
        }


class CustomUserEditForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'is_staff']