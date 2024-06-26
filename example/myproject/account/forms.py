from django import forms
from django.contrib.auth import get_user_model
from .models import UserType


class UserRegisterForm(forms.ModelForm):
    user_type = forms.ChoiceField(
        label="ユーザー種別", choices=UserType.choices, required=True
    )
    # パスワード入力はPasswordInputウィジェットを使う
    password = forms.CharField(label="パスワード", widget=forms.PasswordInput)

    class Meta:
        # ユーザーモデルを取得
        model = get_user_model()
        fields = ["username", "password", "user_type"]
