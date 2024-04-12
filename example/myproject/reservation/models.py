from django.db import models
from django.contrib.auth.models import User
from account.models import UserType


class Room(models.Model):
    """会議室"""

    name = models.CharField("会議室名", max_length=50)
    available_user_type = models.PositiveSmallIntegerField(
        "利用可能ユーザー種別", default=0, choices=UserType.choices
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = verbose_name_plural = "会議室"


class Reservation(models.Model):
    """予約"""

    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __str__(self):
        return f"{self.room} {self.start} - {self.end} by {self.user}"

    class Meta:
        verbose_name = verbose_name_plural = "予約"
