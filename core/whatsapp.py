"""Click-to-chat helpers for the business WhatsApp number.

The number is stored on the owner dashboard (BusinessSettings.whatsapp_number)
so the client can change it without a redeploy; settings.NATURALE_MAY_WHATSAPP
is only a fallback for when no dashboard record exists yet.
"""

from urllib.parse import quote

from django.conf import settings


def business_whatsapp_number():
    from owner.models import BusinessSettings

    business_settings = BusinessSettings.objects.filter(pk=1).first()

    number = ""
    if business_settings and business_settings.whatsapp_number:
        number = business_settings.whatsapp_number
    else:
        number = getattr(settings, "NATURALE_MAY_WHATSAPP", "")

    return "".join(char for char in str(number) if char.isdigit())


def whatsapp_url(message):
    """Return a wa.me link that opens the business DM pre-filled with message.

    Returns an empty string when no business number is configured.
    """
    number = business_whatsapp_number()
    if not number:
        return ""

    return f"https://wa.me/{number}?text={quote(message)}"
