from django import forms

from .models import Product, ProductCategory, ProductImage


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
                    "placeholder": "Describe the product benefits...",
                }
            ),

            "usage_instructions": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Explain how customers should use the product...",
                }
            ),

            "main_image": forms.ClearableFileInput(),

            "is_featured": forms.CheckboxInput(),

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
                    "placeholder": "Describe the image",
                }
            ),
        }