from django.db import models


class Testimonial(models.Model):
    customer_name = models.CharField(max_length=150)

    message = models.TextField()

    photo = models.ImageField(
        upload_to="testimonials/",
        blank=True,
        null=True
    )

    rating = models.PositiveSmallIntegerField(
        default=5
    )

    is_featured = models.BooleanField(
        default=False
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.customer_name
    
class SiteSettings(models.Model):
    business_name = models.CharField(
        max_length=150,
        default="Natural May"
    )

    tagline = models.CharField(
        max_length=255,
        default="Restoring Confidence Through Nature"
    )

    logo = models.ImageField(
        upload_to="site/",
        blank=True,
        null=True
    )

    email = models.EmailField(
        blank=True
    )

    phone = models.CharField(
        max_length=30,
        blank=True
    )

    whatsapp = models.CharField(
        max_length=30,
        blank=True
    )

    address = models.TextField(
        blank=True
    )

    instagram = models.URLField(
        blank=True
    )

    facebook = models.URLField(
        blank=True
    )

    tiktok = models.URLField(
        blank=True
    )

    business_hours = models.TextField(
        blank=True
    )

    about_text = models.TextField(
        blank=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.business_name