from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect

from .forms import ContactMessageForm


def contact(request):

    if request.method == "POST":

        form = ContactMessageForm(request.POST)

        if form.is_valid():

            contact_message = form.save()

            if settings.OWNER_NOTIFICATION_EMAIL:
                send_mail(
                    subject=(
                        "Naturale May contact: "
                        f"{contact_message.subject or contact_message.name}"
                    ),
                    message=(
                        f"Name: {contact_message.name}\n"
                        f"Email: {contact_message.email}\n"
                        f"Phone: {contact_message.phone}\n\n"
                        f"{contact_message.message}"
                    ),
                    from_email=None,
                    recipient_list=[settings.OWNER_NOTIFICATION_EMAIL],
                    fail_silently=True,
                )

            return redirect(
                "contact:success"
            )

    else:

        form = ContactMessageForm()

    return render(
        request,
        "contact/contact.html",
        {
            "form": form,
        }
    )


def contact_success(request):

    return render(
        request,
        "contact/success.html"
    )