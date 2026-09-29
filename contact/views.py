from django.shortcuts import render, redirect

from core.notifications import send_owner_whatsapp
from .forms import ContactMessageForm


def contact(request):

    if request.method == "POST":

        form = ContactMessageForm(request.POST)

        if form.is_valid():

            contact_message = form.save()

            send_owner_whatsapp(
                "*Naturale May - New contact message*\n\n"
                f"Name: {contact_message.name}\n"
                f"Email: {contact_message.email}\n"
                f"Phone: {contact_message.phone}\n"
                f"Subject: {contact_message.subject or '-'}\n\n"
                f"{contact_message.message}"
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