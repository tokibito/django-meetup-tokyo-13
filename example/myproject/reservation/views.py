from typing import Any
from django.urls import reverse_lazy
from django.forms import BaseModelForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from account import models as account_models
from account.decorators import user_profile_required
from . import models
from . import forms


@method_decorator([login_required, user_profile_required], name="dispatch")
class RoomListView(generic.ListView):
    model = models.Room
    template_name = "reservation/index.html"

    def get_queryset(self):
        user_profile = self.request.user.user_profile
        # ユーザー種別によって利用可能な部屋を絞り込む
        if user_profile.user_type == account_models.UserType.NORMAL:
            available_rooms = models.Room.objects.filter(
                available_user_type=account_models.UserType.NORMAL
            )
        else:
            available_rooms = models.Room.objects.all()
        return available_rooms


@method_decorator([login_required, user_profile_required], name="dispatch")
class ReservationView(generic.CreateView):
    model = models.Reservation
    template_name = "reservation/reservation.html"
    form_class = forms.ReservationForm
    success_url = reverse_lazy("my_reservation")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        kwargs["room"] = self.room
        return super().get_context_data(**kwargs)

    def dispatch(self, request, room_id: int):
        user_profile = self.request.user.user_profile
        # ユーザー種別によって利用可能な部屋を絞り込む
        if user_profile.user_type == account_models.UserType.NORMAL:
            available_rooms = models.Room.objects.filter(
                available_user_type=account_models.UserType.NORMAL
            )
        else:
            available_rooms = models.Room.objects.all()
        self.room = get_object_or_404(available_rooms, pk=room_id)
        return super().dispatch(request)

    def form_valid(self, form: BaseModelForm):
        instance = form.save(commit=False)
        instance.room = self.room
        instance.user = self.request.user
        return super().form_valid(form)


class MyReservationListView(generic.ListView, LoginRequiredMixin):
    model = models.Reservation
    template_name = "reservation/my_reservation_list.html"

    def get_queryset(self) -> Any:
        return models.Reservation.objects.filter(user=self.request.user)
