"""Owner notifications via CallMeBot's free WhatsApp API.

Setup: the owner adds +34 644 51 95 23 to their WhatsApp contacts,
sends it any message once, and receives an API key in reply.
The key and phone number are configured through the
WHATSAPP_APIKEY and OWNER_WHATSAPP_NUMBER settings.
"""

import logging
from urllib.parse import urlencode
from urllib.request import urlopen

from django.conf import settings

logger = logging.getLogger(__name__)

CALLMEBOT_URL = "https://api.callmebot.com/whatsapp.php"


def send_owner_whatsapp(text):
    phone = getattr(settings, "OWNER_WHATSAPP_NUMBER", "")
    api_key = getattr(settings, "WHATSAPP_APIKEY", "")

    if not phone or not api_key or not text:
        return

    query = urlencode({
        "phone": phone,
        "apikey": api_key,
        "text": text,
    })

    try:
        urlopen(f"{CALLMEBOT_URL}?{query}", timeout=10)
    except Exception:
        logger.exception("CallMeBot WhatsApp notification failed")
