from django.contrib import admin

from .models import Testimonial, SiteSettings


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = (
        "customer_name",
        "rating",
        "is_featured",
        "is_active",
        "created_at",
    )

    list_filter = (
        "rating",
        "is_featured",
        "is_active",
    )

    search_fields = (
        "customer_name",
        "message",
    )

    readonly_fields = (
        "created_at",
    )


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = (
        "business_name",
        "email",
        "phone",
        "updated_at",
    )

    readonly_fields = (
        "updated_at",
    )