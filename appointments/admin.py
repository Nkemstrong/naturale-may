from django.contrib import admin
from django.utils.html import format_html
from urllib.parse import quote

from .models import Customer, Appointment


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "phone",
        "email",
        "created_at",
    )

    search_fields = (
        "full_name",
        "phone",
        "email",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):

    list_display = (
        "customer",
        "service",
        "appointment_date",
        "appointment_time",
        "status",
        "whatsapp_action",
        "created_at",
    )

    list_filter = (
        "status",
        "service",
        "appointment_date",
    )

    search_fields = (
        "customer__full_name",
        "customer__phone",
        "customer__email",
        "service__name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    date_hierarchy = "appointment_date"

    ordering = (
        "appointment_date",
        "appointment_time",
    )

    @admin.display(
        description="WhatsApp"
    )
    def whatsapp_action(self, obj):

        phone = obj.customer.phone

        # Remove spaces and common phone formatting
        phone = (
            phone.replace(" ", "")
            .replace("-", "")
            .replace("(", "")
            .replace(")", "")
        )

        # Convert Nigerian local number to international format
        if phone.startswith("0"):
            phone = "234" + phone[1:]

        message = (
            f"Hello {obj.customer.full_name},\n\n"
            f"Your appointment with Natural May has been "
            f"{obj.get_status_display().lower()}.\n\n"
            f"Service: {obj.service.name}\n"
            f"Date: {obj.appointment_date.strftime('%A, %B %d, %Y')}\n"
            f"Time: {obj.appointment_time.strftime('%I:%M %p')}\n\n"
        )

        if obj.status == "confirmed":
            message += (
                "We look forward to seeing you. "
                "Thank you for choosing Natural May."
            )

        elif obj.status == "cancelled":
            message += (
                "Unfortunately, this appointment has been "
                "cancelled. Please contact us if you would "
                "like to choose another date or time."
            )

        else:
            message += (
                "Please contact Natural May if you need "
                "any further information."
            )

        whatsapp_url = (
            "https://wa.me/"
            f"{phone}?text={quote(message)}"
        )

        return format_html(
            '<a href="{}" target="_blank" '
            'style="color:#25D366;font-weight:600;">'
            '💬 WhatsApp'
            '</a>',
            whatsapp_url,
        )