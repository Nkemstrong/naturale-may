from django.db import models


class BusinessSettings(models.Model):
    """
    Stores the main business information used across the website.

    Only one BusinessSettings record should normally exist.
    """

    bank_name = models.CharField(
        max_length=150,
        default="Wema Bank"
    )

    account_name = models.CharField(
        max_length=150,
        default="Naturale May Business Enterprise"
    )

    account_number = models.CharField(
        max_length=50,
        default="0423979574"
    )

    whatsapp_number = models.CharField(
        max_length=30,
        default="2347037305041"
    )

    business_phone = models.CharField(
        max_length=30,
        blank=True
    )

    business_email = models.EmailField(
        blank=True
    )

    business_address = models.TextField(
        default="46 Aba-Owerri Road, close to Brass Junction, Aba"
    )

    payment_instructions = models.TextField(
        blank=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return "Naturale May Business Settings"

    class Meta:
        verbose_name = "Business Settings"
        verbose_name_plural = "Business Settings"