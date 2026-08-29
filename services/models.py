from django.db import models
from django.urls import reverse


class Service(models.Model):

    PRICE_DISPLAY_CHOICES = [
        ("price", "Show Price"),
        ("contact", "Contact for Price"),
        ("coming_soon", "Coming Soon"),
    ]

    name = models.CharField(max_length=200)

    slug = models.SlugField(
        max_length=220,
        unique=True
    )

    short_description = models.CharField(
        max_length=300,
        blank=True
    )

    description = models.TextField()

    price_display = models.CharField(
        max_length=20,
        choices=PRICE_DISPLAY_CHOICES,
        default="price"
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    duration = models.PositiveIntegerField(
        help_text="Duration in minutes.",
        blank=True,
        null=True
    )

    image = models.ImageField(
        upload_to="services/",
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            "services:detail",
            kwargs={"slug": self.slug}
        )