from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "username",
            "full_name",
            "email",
            "password1",
            "password2",
        ]

    full_name = forms.CharField(
        max_length=100,
        required=False,
        help_text="Optional.",
        label="이름",
    )
    username = forms.CharField(
        max_length=150,
        required=False,
        help_text="Optional.",
        label="유저명",
    )
    email = forms.EmailField(
        max_length=254,
        help_text="Required. Inform a valid email address",
        label="이메일",
    )
