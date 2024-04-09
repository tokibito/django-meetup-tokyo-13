from typing import Any
from django.forms import BaseModelForm
from django.http import HttpRequest
from django.http.response import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from . import models
from . import forms

class RoomListView(generic.ListView):
    model = models.Room
    template_name = "reservation/index.html"

class ReservationView(generic.CreateView, LoginRequiredMixin):
    model = models.Reservation
    template_name = "reservation/reservation.html"
    form_class = forms.ReservationForm
    success_url = "/"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        kwargs["room"] = self.room
        return super().get_context_data(**kwargs)

    def dispatch(self, request: HttpRequest, room_id: int) -> HttpResponse:
        self.room = models.Room.objects.get(pk=room_id)
        return super().dispatch(request)

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        instance = form.save(commit=False)
        instance.room = self.room
        instance.user = self.request.user
        return super().form_valid(form)

class MyReservationListView(generic.ListView, LoginRequiredMixin):
    model = models.Reservation
    template_name = "reservation/my_reservation_list.html"

    def get_queryset(self) -> Any:
        return models.Reservation.objects.filter(user=self.request.user)