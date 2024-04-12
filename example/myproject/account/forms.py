from django import forms
from django.conf import settings
from .models import UserType


class UserRegisterForm(forms.ModelForm):
    user_type = forms.ChoiceField(
        label="ユーザー種別", choices=UserType.choices, required=True
    )

    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ["username", "password", "user_type"]
