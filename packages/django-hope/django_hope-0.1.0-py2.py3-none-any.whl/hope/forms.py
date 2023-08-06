"""Forms module."""

from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class SignUpForm(UserCreationForm):
    """Simple sign-up form overriding the basic Django user creation form."""

    email = forms.EmailField(label='Email', max_length=254)

    class Meta:
        """Django meta-class."""

        model = User
        fields = ('username', 'email', 'password1', 'password2', )
