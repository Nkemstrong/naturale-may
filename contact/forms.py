from django import forms

from .models import ContactMessage


class ContactMessageForm(forms.ModelForm):

    class Meta:
        model = ContactMessage

        fields = [
            "name",
            "email",
            "phone",
            "subject",
            "message",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Your full name",
                    "autocomplete": "name",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "placeholder": "you@example.com",
                    "autocomplete": "email",
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "placeholder": "07037305041",
                    "autocomplete": "tel",
                }
            ),

            "subject": forms.TextInput(
                attrs={
                    "placeholder": "How can we help you?",
                }
            ),

            "message": forms.Textarea(
                attrs={
                    "placeholder": "Write your message here...",
                    "rows": 6,
                }
            ),
        }