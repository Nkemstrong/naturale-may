from django.db import IntegrityError, transaction
from django.shortcuts import render, redirect

from core.whatsapp import whatsapp_url
from .forms import AppointmentForm
from .models import Customer, Appointment


def book_appointment(request):

    if request.method == "POST":

        form = AppointmentForm(request.POST)

        if form.is_valid():

            try:

                with transaction.atomic():

                    customer = Customer.objects.create(
                        full_name=form.cleaned_data["full_name"],
                        phone=form.cleaned_data["phone"],
                        email=form.cleaned_data["email"],
                    )

                    appointment = Appointment.objects.create(
                        customer=customer,
                        service=form.cleaned_data["service"],
                        appointment_date=form.cleaned_data[
                            "appointment_date"
                        ],
                        appointment_time=form.cleaned_data[
                            "appointment_time"
                        ],
                        notes=form.cleaned_data["notes"],
                    )

                message = (
                    "Hello Naturale May! 👋\n\n"
                    "I have just submitted an appointment request "
                    "through the Naturale May website.\n\n"
                    f"Name: {appointment.customer.full_name}\n"
                    f"Phone: {appointment.customer.phone}\n"
                    f"Service: {appointment.service.name}\n"
                    f"Date: {appointment.appointment_date.strftime('%B %d, %Y')}\n"
                    f"Time: {appointment.appointment_time.strftime('%I:%M %p')}\n"
                )

                if appointment.notes:
                    message += f"Notes: {appointment.notes}\n"

                message += "\nPlease confirm my appointment. Thank you! 🌿"

                url = whatsapp_url(message)
                if url:
                    return redirect(url)

                return redirect(
                    "appointments:success",
                    pk=appointment.pk,
                )

            except IntegrityError:

                form.add_error(
                    None,
                    "Sorry, that appointment time was just booked. "
                    "Please choose another time."
                )

    else:

        form = AppointmentForm()

    return render(
        request,
        "appointments/book.html",
        {
            "form": form,
        }
    )


def booking_success(request, pk):

    from django.shortcuts import get_object_or_404

    appointment = get_object_or_404(
        Appointment.objects.select_related(
            "customer",
            "service",
        ),
        pk=pk,
    )

    return render(
        request,
        "appointments/success.html",
        {
            "appointment": appointment,
        }
    )