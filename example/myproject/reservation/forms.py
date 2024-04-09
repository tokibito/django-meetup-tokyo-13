from django import forms

from . import models

class ReservationForm(forms.ModelForm):
    class Meta:
        model = models.Reservation
        fields = ["start", "end"]
        widgets = {
            "start": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }