from django.urls import path

from . import views


app_name = "appointments"


urlpatterns = [
    path(
        "",
        views.book_appointment,
        name="book"
    ),

    path(
        "success/<int:pk>/",
        views.booking_success,
        name="success"
    ),
]