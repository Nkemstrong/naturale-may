from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include


urlpatterns = [
    # ==============================
    # NATURAL MAY OWNER DASHBOARD
    # ==============================
    path(
        "dashboard/",
        include("owner.urls"),
    ),

    # Public website
    path(
        "",
        include("core.urls"),
    ),

    path(
        "shop/",
        include("products.urls"),
    ),

    path(
        "services/",
        include("services.urls"),
    ),

    path(
        "appointments/",
        include("appointments.urls"),
    ),

    path(
        "contact/",
        include("contact.urls"),
    ),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
