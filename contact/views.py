from django.shortcuts import render, redirect

from core.whatsapp import whatsapp_url
from .forms import ContactMessageForm


def contact(request):

    if request.method == "POST":

        form = ContactMessageForm(request.POST)

        if form.is_valid():

            contact_message = form.save()

            message = (
                "Hello Naturale May! 👋\n\n"
                "I just submitted the contact form on your website.\n\n"
                f"Name: {contact_message.name}\n"
                f"Email: {contact_message.email}\n"
                f"Phone: {contact_message.phone or '-'}\n"
                f"Subject: {contact_message.subject or '-'}\n\n"
                f"Message:\n{contact_message.message}"
            )

            url = whatsapp_url(message)
            if url:
                return redirect(url)

            return redirect("contact:success")

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
