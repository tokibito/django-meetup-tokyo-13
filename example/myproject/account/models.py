from django.db import models
from django.conf import settings


class UserType(models.IntegerChoices):
    """ユーザー種別"""

    NORMAL = 1, "一般"
    ADVANCED = 2, "上級"


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="ユーザー",
        related_name="user_profile",
    )
    user_type = models.PositiveSmallIntegerField(
        "ユーザー種別", default=0, choices=UserType.choices
    )

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = verbose_name_plural = "ユーザープロフィール"


def get_user_profile(user):
    """ユーザープロフィールを取得する"""
    try:
        return user.user_profile
    except user.__class__.user_profile.RelatedObjectDoesNotExist:
        pass
