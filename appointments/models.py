from django.db import models
from django.core.exceptions import ValidationError
from django.urls import reverse

from services.models import Service


class Customer(models.Model):
    full_name = models.CharField(max_length=150)

    phone = models.CharField(max_length=30)

    email = models.EmailField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.full_name
    
    @property
    def whatsapp_number(self):
        """
        Return the customer's phone number in international format
        for WhatsApp.
        """
        phone = "".join(
            character
            for character in self.phone
            if character.isdigit()
        )

        if phone.startswith("0"):
            return "234" + phone[1:]

        if phone.startswith("234"):
            return phone

        return phone
        
class Appointment(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="appointments"
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.PROTECT,
        related_name="appointments"
    )

    appointment_date = models.DateField()

    appointment_time = models.TimeField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = [
            "-appointment_date",
            "-appointment_time",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "appointment_date",
                    "appointment_time",
                ],
                name="unique_appointment_slot"
            )
        ]

    def __str__(self):
        return (
            f"{self.customer.full_name} - "
            f"{self.service.name} - "
            f"{self.appointment_date} "
            f"{self.appointment_time}"
        )

    def get_absolute_url(self):
        return reverse(
            "appointments:detail",
            kwargs={"pk": self.pk}
        )