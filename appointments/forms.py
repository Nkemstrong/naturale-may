from datetime import time

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Appointment


class AppointmentForm(forms.Form):

    full_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Your full name",
                "autocomplete": "name",
            }
        ),
    )

    phone = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "placeholder": "e.g. 08012345678",
                "autocomplete": "tel",
            }
        ),
    )

    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(
            attrs={
                "placeholder": "you@example.com",
                "autocomplete": "email",
            }
        ),
    )

    service = forms.ModelChoiceField(
        queryset=None,
        empty_label="Select a service",
    )

    appointment_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "date",
            }
        )
    )

    appointment_time = forms.TimeField(
        widget=forms.TimeInput(
            attrs={
                "type": "time",
            }
        )
    )

    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "placeholder": (
                    "Anything we should know about your appointment?"
                ),
                "rows": 5,
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        from services.models import Service

        self.fields["service"].queryset = Service.objects.filter(
            is_active=True
        ).order_by("name")

    def clean_appointment_date(self):
        appointment_date = self.cleaned_data["appointment_date"]

        today = timezone.localdate()

        if appointment_date < today:
            raise ValidationError(
                "Please select today or a future date."
            )

        # Sunday = 6
        if appointment_date.weekday() == 6:
            raise ValidationError(
                "Appointments are not available on Sundays."
            )

        return appointment_date

    def clean(self):
        cleaned_data = super().clean()

        appointment_date = cleaned_data.get("appointment_date")
        appointment_time = cleaned_data.get("appointment_time")

        if not appointment_date or not appointment_time:
            return cleaned_data

        # Business hours
        opening_time = time(9, 0)
        closing_time = time(18, 0)

        if not opening_time <= appointment_time <= closing_time:
            self.add_error(
                "appointment_time",
                "Appointments are available between 9:00 AM and 6:00 PM."
            )

        # Only allow appointments on the hour or half-hour.
        if appointment_time.minute not in (0, 30):
            self.add_error(
                "appointment_time",
                "Please select an appointment time on the hour "
                "or half-hour."
            )

        # Prevent booking a time that has already passed today.
        today = timezone.localdate()
        current_time = timezone.localtime().time()

        if appointment_date == today and appointment_time <= current_time:
            self.add_error(
                "appointment_time",
                "Please select a future appointment time."
            )

        # Prevent double booking.
        existing_appointment = Appointment.objects.filter(
            appointment_date=appointment_date,
            appointment_time=appointment_time,
        ).exclude(
            status="cancelled"
        ).exists()

        if existing_appointment:
            self.add_error(
                "appointment_time",
                "Sorry, this time is already booked. "
                "Please choose another time."
            )

        return cleaned_data