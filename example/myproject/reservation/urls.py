from django.urls import path
from . import views

urlpatterns = [
    path("", views.RoomListView.as_view(), name="index"),
    path("reservation/<int:room_id>/", views.ReservationView.as_view(), name="reservation"),
    path("my_reservation/", views.MyReservationListView.as_view(), name="my_reservation"),
]
