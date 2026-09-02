from django import forms
from django.db import models

from .models import BusinessSettings

from products.models import (
    Product,
    ProductCategory,
    ProductImage,
)
from services.models import Service


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = [
            "name",
            "slug",
            "short_description",
            "description",
            "price_display",
            "price",
            "duration",
            "image",
            "is_active",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "e.g. Natural Hair Treatment",
                }
            ),
            "slug": forms.TextInput(
                attrs={
                    "placeholder": "e.g. natural-hair-treatment",
                }
            ),
            "short_description": forms.TextInput(
                attrs={
                    "placeholder": "Short description of the service",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "rows": 5,
                    "placeholder": "Describe the service...",
                }
            ),
            "price_display": forms.Select(),
            "price": forms.NumberInput(
                attrs={
                    "placeholder": "0.00",
                    "step": "0.01",
                    "min": "0",
                }
            ),
            "duration": forms.NumberInput(
                attrs={
                    "placeholder": "Duration in minutes",
                    "min": "1",
                }
            ),
            "image": forms.ClearableFileInput(),
            "is_active": forms.CheckboxInput(),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "category",
            "name",
            "slug",
            "short_description",
            "description",
            "price",
            "stock_status",
            "ingredients",
            "benefits",
            "usage_instructions",
            "main_image",
            "is_featured",
            "is_active",
        ]

        widgets = {
            "category": forms.Select(),
            "name": forms.TextInput(
                attrs={
                    "placeholder": "e.g. Natural Hair Growth Oil",
                }
            ),
            "slug": forms.TextInput(
                attrs={
                    "placeholder": "e.g. natural-hair-growth-oil",
                }
            ),
            "short_description": forms.TextInput(
                attrs={
                    "placeholder": "Short description of the product",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "rows": 5,
                    "placeholder": "Describe the product...",
                }
            ),
            "price": forms.NumberInput(
                attrs={
                    "placeholder": "0.00",
                    "step": "0.01",
                    "min": "0",
                }
            ),
            "stock_status": forms.Select(),
            "ingredients": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "List the ingredients...",
                }
            ),
            "benefits": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Describe the benefits...",
                }
            ),
            "usage_instructions": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Explain how customers should use this product...",
                }
            ),
            "main_image": forms.ClearableFileInput(),
            "is_featured": forms.CheckboxInput(),
            "is_active": forms.CheckboxInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["category"].queryset = (
            ProductCategory.objects
            .filter(is_active=True)
            .order_by("name")
        )

        # If editing a product whose category has been
        # deactivated, keep that category available.
        if self.instance and self.instance.pk:
            current_category = self.instance.category

            if current_category and not current_category.is_active:
                self.fields["category"].queryset = (
                    ProductCategory.objects
                    .filter(
                        models.Q(is_active=True)
                        | models.Q(pk=current_category.pk)
                    )
                    .order_by("name")
                )


class ProductCategoryForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = [
            "name",
            "slug",
            "description",
            "image",
            "is_active",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "e.g. Hair Care",
                }
            ),
            "slug": forms.TextInput(
                attrs={
                    "placeholder": "e.g. hair-care",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Describe this product category...",
                }
            ),
            "image": forms.ClearableFileInput(),
            "is_active": forms.CheckboxInput(),
        }


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = [
            "image",
            "alt_text",
        ]

        widgets = {
            "image": forms.ClearableFileInput(),
            "alt_text": forms.TextInput(
                attrs={
                    "placeholder": "Describe this image",
                }
            ),
        }
        
class BusinessSettingsForm(forms.ModelForm):
    class Meta:
        model = BusinessSettings
        fields = [
            "bank_name",
            "account_name",
            "account_number",
            "whatsapp_number",
            "business_phone",
            "business_email",
            "business_address",
            "payment_instructions",
        ]

        widgets = {
            "bank_name": forms.TextInput(
                attrs={
                    "placeholder": "e.g. Wema Bank",
                }
            ),
            "account_name": forms.TextInput(
                attrs={
                    "placeholder": "e.g. Naturale May Business Enterprise",
                }
            ),
            "account_number": forms.TextInput(
                attrs={
                    "placeholder": "e.g. 0423979574",
                }
            ),
            "whatsapp_number": forms.TextInput(
                attrs={
                    "placeholder": "e.g. 2347037305041",
                }
            ),
            "business_phone": forms.TextInput(
                attrs={
                    "placeholder": "Business phone number",
                }
            ),
            "business_email": forms.EmailInput(
                attrs={
                    "placeholder": "Business email address",
                }
            ),
            "business_address": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "e.g. 46 Aba-Owerri Road, close to Brass Junction, Aba",
                }
            ),
            "payment_instructions": forms.Textarea(
                attrs={
                    "rows": 5,
                    "placeholder": "Add any instructions customers should follow after making payment...",
                }
            ),
        }