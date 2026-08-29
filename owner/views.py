from urllib.parse import quote

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.db import models
from django.db.models import Count, Q
from django.db.models.deletion import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from appointments.models import Appointment, Customer
from contact.models import ContactMessage
from products.models import Product, ProductCategory, ProductImage
from services.models import Service

from .forms import (
    ProductCategoryForm,
    ProductForm,
    ProductImageForm,
    ServiceForm,
)


# ============================================================
# OWNER ACCESS CONTROL
# ============================================================

def owner_required(view_func):
    return user_passes_test(
        lambda user: user.is_authenticated and user.is_staff,
        login_url="owner:login",
    )(view_func)


# ============================================================
# OWNER LOGIN / LOGOUT
# ============================================================

def owner_login(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect("owner:dashboard")

        logout(request)

    error = None

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None and user.is_staff:
            login(request, user)
            return redirect("owner:dashboard")

        error = "Invalid login details or you do not have owner access."

    return render(
        request,
        "owner/login.html",
        {
            "error": error,
        },
    )


@owner_required
def owner_logout(request):
    logout(request)
    return redirect("owner:login")


# ============================================================
# DASHBOARD
# ============================================================

@owner_required
def dashboard(request):

    # --------------------------------------------------------
    # BASE APPOINTMENTS QUERYSET
    # --------------------------------------------------------

    appointments = (
        Appointment.objects
        .select_related("customer", "service")
        .order_by(
            "appointment_date",
            "appointment_time",
        )
    )

    # --------------------------------------------------------
    # SEARCH
    # --------------------------------------------------------

    search_query = request.GET.get("search", "").strip()

    if search_query:
        appointments = appointments.filter(
            Q(customer__full_name__icontains=search_query)
            | Q(customer__phone__icontains=search_query)
            | Q(customer__email__icontains=search_query)
            | Q(service__name__icontains=search_query)
        )

    # --------------------------------------------------------
    # STATUS FILTER
    # --------------------------------------------------------

    status_filter = request.GET.get("status", "").strip()

    allowed_statuses = [
        "pending",
        "confirmed",
        "completed",
        "cancelled",
    ]

    if status_filter in allowed_statuses:
        appointments = appointments.filter(
            status=status_filter
        )

    # --------------------------------------------------------
    # DATE FILTER
    # --------------------------------------------------------

    date_filter = request.GET.get("date", "").strip()

    if date_filter:
        appointments = appointments.filter(
            appointment_date=date_filter
        )

    # --------------------------------------------------------
    # TODAY'S APPOINTMENTS
    # --------------------------------------------------------

    today = timezone.localdate()

    today_appointments = (
        Appointment.objects
        .select_related("customer", "service")
        .filter(
            appointment_date=today
        )
        .exclude(
            status="cancelled"
        )
        .order_by(
            "appointment_time"
        )
    )

    # --------------------------------------------------------
    # WHATSAPP LINKS
    # --------------------------------------------------------

    for appointment in appointments:

        phone = appointment.customer.phone.strip()

        phone = "".join(
            character
            for character in phone
            if character.isdigit()
        )

        # Convert Nigerian numbers such as 08012345678
        # to international format 2348012345678
        if phone.startswith("0"):
            phone = "234" + phone[1:]

        message = (
            f"Hello {appointment.customer.full_name}, "
            f"this is Natural May. "
            f"We are following up on your appointment for "
            f"{appointment.service.name} on "
            f"{appointment.appointment_date.strftime('%B %d, %Y')} "
            f"at "
            f"{appointment.appointment_time.strftime('%I:%M %p')}. "
            f"Thank you for choosing Natural May."
        )

        appointment.whatsapp_url = (
            f"https://wa.me/{phone}"
            f"?text={quote(message)}"
        )

    # --------------------------------------------------------
    # ALL APPOINTMENTS
    # --------------------------------------------------------

    all_appointments = Appointment.objects.all()

    # --------------------------------------------------------
    # APPOINTMENT STATISTICS
    # --------------------------------------------------------

    total_appointments = all_appointments.count()

    pending_count = all_appointments.filter(
        status="pending"
    ).count()

    confirmed_count = all_appointments.filter(
        status="confirmed"
    ).count()

    completed_count = all_appointments.filter(
        status="completed"
    ).count()

    cancelled_count = all_appointments.filter(
        status="cancelled"
    ).count()

    # --------------------------------------------------------
    # CUSTOMERS
    # --------------------------------------------------------

    total_customers = Customer.objects.count()

    # --------------------------------------------------------
    # PRODUCTS
    # --------------------------------------------------------

    total_products = Product.objects.count()

    # --------------------------------------------------------
    # SERVICES
    # --------------------------------------------------------

    total_services = Service.objects.count()

    # --------------------------------------------------------
    # MESSAGES
    # --------------------------------------------------------

    total_messages = ContactMessage.objects.count()

    unread_messages = ContactMessage.objects.filter(
        is_read=False
    ).count()

    # --------------------------------------------------------
    # THIS MONTH
    # --------------------------------------------------------

    month_start = today.replace(day=1)

    this_month_appointments = all_appointments.filter(
        appointment_date__gte=month_start,
        appointment_date__lte=today,
    ).count()

    # --------------------------------------------------------
    # MOST BOOKED SERVICE
    # --------------------------------------------------------

    popular_service = (
        Service.objects
        .annotate(
            booking_count=Count("appointments")
        )
        .order_by("-booking_count")
        .first()
    )

    # --------------------------------------------------------
    # CONTEXT
    # --------------------------------------------------------

    context = {
        # Appointments
        "appointments": appointments,
        "today_appointments": today_appointments,

        # Appointment statistics
        "today_count": today_appointments.count(),
        "pending_count": pending_count,
        "confirmed_count": confirmed_count,
        "completed_count": completed_count,
        "cancelled_count": cancelled_count,

        # Business statistics
        "total_appointments": total_appointments,
        "total_customers": total_customers,
        "total_products": total_products,
        "total_services": total_services,
        "total_messages": total_messages,
        "unread_messages": unread_messages,
        "this_month_appointments": this_month_appointments,
        "popular_service": popular_service,

        # Filters
        "search_query": search_query,
        "status_filter": status_filter,
        "date_filter": date_filter,
    }

    return render(
        request,
        "owner/dashboard.html",
        context,
    )


# ============================================================
# APPOINTMENT STATUS
# ============================================================

@owner_required
def update_appointment_status(request, pk):

    if request.method != "POST":
        return redirect("owner:dashboard")

    appointment = get_object_or_404(
        Appointment,
        pk=pk,
    )

    new_status = request.POST.get("status")

    allowed_statuses = [
        "pending",
        "confirmed",
        "completed",
        "cancelled",
    ]

    if new_status in allowed_statuses:

        appointment.status = new_status

        appointment.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        messages.success(
            request,
            f"Appointment status updated to {new_status}.",
        )

    else:
        messages.error(
            request,
            "Invalid appointment status.",
        )

    return redirect("owner:dashboard")


# ============================================================
# SERVICES
# ============================================================

@owner_required
def services_list(request):

    services = (
        Service.objects
        .all()
        .order_by("name")
    )

    return render(
        request,
        "owner/services/list.html",
        {
            "services": services,
        },
    )


@owner_required
def service_create(request):

    if request.method == "POST":

        form = ServiceForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            service = form.save()

            messages.success(
                request,
                f"{service.name} was added successfully.",
            )

            return redirect("owner:services_list")

    else:
        form = ServiceForm()

    return render(
        request,
        "owner/services/form.html",
        {
            "form": form,
            "page_title": "Add Service",
            "submit_text": "Add Service",
        },
    )


@owner_required
def service_edit(request, pk):

    service = get_object_or_404(
        Service,
        pk=pk,
    )

    if request.method == "POST":

        form = ServiceForm(
            request.POST,
            request.FILES,
            instance=service,
        )

        if form.is_valid():

            service = form.save()

            messages.success(
                request,
                f"{service.name} was updated successfully.",
            )

            return redirect("owner:services_list")

    else:
        form = ServiceForm(
            instance=service,
        )

    return render(
        request,
        "owner/services/form.html",
        {
            "form": form,
            "service": service,
            "page_title": "Edit Service",
            "submit_text": "Save Changes",
        },
    )


@owner_required
def service_toggle(request, pk):

    if request.method == "POST":

        service = get_object_or_404(
            Service,
            pk=pk,
        )

        service.is_active = not service.is_active

        service.save(
            update_fields=[
                "is_active",
                "updated_at",
            ]
        )

        status = (
            "activated"
            if service.is_active
            else "deactivated"
        )

        messages.success(
            request,
            f"{service.name} was {status}.",
        )

    return redirect("owner:services_list")


@owner_required
def service_delete(request, pk):

    service = get_object_or_404(
        Service,
        pk=pk,
    )

    if request.method == "POST":

        service_name = service.name

        service.delete()

        messages.success(
            request,
            f"{service_name} was deleted.",
        )

        return redirect("owner:services_list")

    return render(
        request,
        "owner/services/delete.html",
        {
            "service": service,
        },
    )


# ============================================================
# PRODUCTS
# ============================================================

@owner_required
def products_list(request):

    products = (
        Product.objects
        .select_related("category")
        .order_by("-created_at")
    )

    return render(
        request,
        "owner/products/list.html",
        {
            "products": products,
        },
    )


@owner_required
def product_create(request):

    if request.method == "POST":

        form = ProductForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            product = form.save()

            messages.success(
                request,
                f"{product.name} was added successfully.",
            )

            return redirect("owner:products_list")

    else:
        form = ProductForm()

    return render(
        request,
        "owner/products/form.html",
        {
            "form": form,
            "page_title": "Add Product",
            "submit_text": "Add Product",
        },
    )


@owner_required
def product_edit(request, pk):

    product = get_object_or_404(
        Product,
        pk=pk,
    )

    if request.method == "POST":

        form = ProductForm(
            request.POST,
            request.FILES,
            instance=product,
        )

        if form.is_valid():

            product = form.save()

            messages.success(
                request,
                f"{product.name} was updated successfully.",
            )

            return redirect("owner:products_list")

    else:
        form = ProductForm(
            instance=product,
        )

    return render(
        request,
        "owner/products/form.html",
        {
            "form": form,
            "product": product,
            "page_title": "Edit Product",
            "submit_text": "Save Changes",
        },
    )


@owner_required
def product_toggle(request, pk):

    if request.method == "POST":

        product = get_object_or_404(
            Product,
            pk=pk,
        )

        product.is_active = not product.is_active

        product.save(
            update_fields=[
                "is_active",
                "updated_at",
            ]
        )

        status = (
            "activated"
            if product.is_active
            else "deactivated"
        )

        messages.success(
            request,
            f"{product.name} was {status}.",
        )

    return redirect("owner:products_list")


@owner_required
def product_feature_toggle(request, pk):

    if request.method == "POST":

        product = get_object_or_404(
            Product,
            pk=pk,
        )

        product.is_featured = not product.is_featured

        product.save(
            update_fields=[
                "is_featured",
                "updated_at",
            ]
        )

        status = (
            "featured"
            if product.is_featured
            else "removed from featured products"
        )

        messages.success(
            request,
            f"{product.name} was {status}.",
        )

    return redirect("owner:products_list")


@owner_required
def product_delete(request, pk):

    product = get_object_or_404(
        Product,
        pk=pk,
    )

    if request.method == "POST":

        product_name = product.name

        product.delete()

        messages.success(
            request,
            f"{product_name} was deleted.",
        )

        return redirect("owner:products_list")

    return render(
        request,
        "owner/products/delete.html",
        {
            "product": product,
        },
    )


# ============================================================
# PRODUCT CATEGORIES
# ============================================================

@owner_required
def categories_list(request):

    categories = (
        ProductCategory.objects
        .prefetch_related("products")
        .order_by("name")
    )

    return render(
        request,
        "owner/products/categories.html",
        {
            "categories": categories,
        },
    )


@owner_required
def category_create(request):

    if request.method == "POST":

        form = ProductCategoryForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            category = form.save()

            messages.success(
                request,
                f"{category.name} was added successfully.",
            )

            return redirect("owner:categories_list")

    else:
        form = ProductCategoryForm()

    return render(
        request,
        "owner/products/category_form.html",
        {
            "form": form,
            "page_title": "Add Category",
            "submit_text": "Add Category",
        },
    )


@owner_required
def category_edit(request, pk):

    category = get_object_or_404(
        ProductCategory,
        pk=pk,
    )

    if request.method == "POST":

        form = ProductCategoryForm(
            request.POST,
            request.FILES,
            instance=category,
        )

        if form.is_valid():

            category = form.save()

            messages.success(
                request,
                f"{category.name} was updated successfully.",
            )

            return redirect("owner:categories_list")

    else:
        form = ProductCategoryForm(
            instance=category,
        )

    return render(
        request,
        "owner/products/category_form.html",
        {
            "form": form,
            "category": category,
            "page_title": "Edit Category",
            "submit_text": "Save Changes",
        },
    )


@owner_required
def category_toggle(request, pk):

    if request.method == "POST":

        category = get_object_or_404(
            ProductCategory,
            pk=pk,
        )

        category.is_active = not category.is_active

        category.save(
            update_fields=[
                "is_active",
            ]
        )

        status = (
            "activated"
            if category.is_active
            else "deactivated"
        )

        messages.success(
            request,
            f"{category.name} was {status}.",
        )

    return redirect("owner:categories_list")


@owner_required
def category_delete(request, pk):

    category = get_object_or_404(
        ProductCategory,
        pk=pk,
    )

    if request.method == "POST":

        category_name = category.name

        try:

            category.delete()

            messages.success(
                request,
                f"{category_name} was deleted.",
            )

            return redirect("owner:categories_list")

        except ProtectedError:

            messages.error(
                request,
                (
                    f"{category_name} cannot be deleted because "
                    "products are currently using this category. "
                    "Deactivate it instead."
                ),
            )

            return redirect("owner:categories_list")

    return render(
        request,
        "owner/products/category_delete.html",
        {
            "category": category,
        },
    )


# ============================================================
# PRODUCT GALLERY
# ============================================================

@owner_required
def product_gallery(request, pk):

    product = get_object_or_404(
        Product,
        pk=pk,
    )

    images = product.images.all()

    return render(
        request,
        "owner/products/gallery.html",
        {
            "product": product,
            "images": images,
        },
    )


@owner_required
def product_image_create(request, pk):

    product = get_object_or_404(
        Product,
        pk=pk,
    )

    if request.method == "POST":

        form = ProductImageForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            image = form.save(
                commit=False
            )

            image.product = product
            image.save()

            messages.success(
                request,
                "Gallery image was added successfully.",
            )

            return redirect(
                "owner:product_gallery",
                pk=product.pk,
            )

    else:
        form = ProductImageForm()

    return render(
        request,
        "owner/products/image_form.html",
        {
            "form": form,
            "product": product,
            "page_title": "Add Gallery Image",
            "submit_text": "Add Image",
        },
    )


@owner_required
def product_image_edit(request, pk):

    image = get_object_or_404(
        ProductImage,
        pk=pk,
    )

    if request.method == "POST":

        form = ProductImageForm(
            request.POST,
            request.FILES,
            instance=image,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Gallery image was updated successfully.",
            )

            return redirect(
                "owner:product_gallery",
                pk=image.product.pk,
            )

    else:
        form = ProductImageForm(
            instance=image,
        )

    return render(
        request,
        "owner/products/image_form.html",
        {
            "form": form,
            "product": image.product,
            "image": image,
            "page_title": "Edit Gallery Image",
            "submit_text": "Save Changes",
        },
    )


@owner_required
def product_image_delete(request, pk):

    image = get_object_or_404(
        ProductImage,
        pk=pk,
    )

    product = image.product

    if request.method == "POST":

        image.delete()

        messages.success(
            request,
            "Gallery image was deleted successfully.",
        )

        return redirect(
            "owner:product_gallery",
            pk=product.pk,
        )

    return render(
        request,
        "owner/products/image_delete.html",
        {
            "image": image,
            "product": product,
        },
    )


# ============================================================
# CONTACT MESSAGES
# ============================================================

@owner_required
def messages_list(request):

    messages_queryset = (
        ContactMessage.objects
        .all()
        .order_by("-created_at")
    )

    search_query = request.GET.get(
        "search",
        "",
    ).strip()

    if search_query:

        messages_queryset = messages_queryset.filter(
            models.Q(
                name__icontains=search_query
            )
            | models.Q(
                email__icontains=search_query
            )
            | models.Q(
                subject__icontains=search_query
            )
            | models.Q(
                message__icontains=search_query
            )
        )

    return render(
        request,
        "owner/messages/list.html",
        {
            "messages": messages_queryset,
            "search_query": search_query,
            "unread_count": ContactMessage.objects.filter(
                is_read=False
            ).count(),
        },
    )


@owner_required
def message_detail(request, pk):

    contact_message = get_object_or_404(
        ContactMessage,
        pk=pk,
    )

    # Automatically mark message as read
    if not contact_message.is_read:

        contact_message.is_read = True

        contact_message.save(
            update_fields=[
                "is_read",
            ]
        )

    return render(
        request,
        "owner/messages/detail.html",
        {
            "contact_message": contact_message,
        },
    )


@owner_required
def message_toggle_read(request, pk):

    if request.method == "POST":

        contact_message = get_object_or_404(
            ContactMessage,
            pk=pk,
        )

        contact_message.is_read = (
            not contact_message.is_read
        )

        contact_message.save(
            update_fields=[
                "is_read",
            ]
        )

        status = (
            "marked as read"
            if contact_message.is_read
            else "marked as unread"
        )

        messages.success(
            request,
            (
                f"Message from {contact_message.name} "
                f"was {status}."
            ),
        )

    return redirect("owner:messages_list")


@owner_required
def message_delete(request, pk):

    contact_message = get_object_or_404(
        ContactMessage,
        pk=pk,
    )

    if request.method == "POST":

        message_name = contact_message.name

        contact_message.delete()

        messages.success(
            request,
            f"Message from {message_name} was deleted.",
        )

        return redirect("owner:messages_list")

    return render(
        request,
        "owner/messages/delete.html",
        {
            "contact_message": contact_message,
        },
    )


# ============================================================
# CUSTOMERS
# ============================================================

@owner_required
def customers_list(request):

    customers = (
        Customer.objects
        .prefetch_related(
            "appointments__service"
        )
        .order_by("-created_at")
    )

    search_query = request.GET.get(
        "search",
        "",
    ).strip()

    if search_query:

        customers = customers.filter(
            Q(full_name__icontains=search_query)
            | Q(phone__icontains=search_query)
            | Q(email__icontains=search_query)
        )

    return render(
        request,
        "owner/customers/list.html",
        {
            "customers": customers,
            "search_query": search_query,
        },
    )


@owner_required
def customer_detail(request, pk):

    customer = get_object_or_404(
        Customer.objects.prefetch_related(
            "appointments__service"
        ),
        pk=pk,
    )

    appointments = (
        customer.appointments
        .select_related("service")
        .order_by(
            "-appointment_date",
            "-appointment_time",
        )
    )

    pending_count = appointments.filter(
        status="pending"
    ).count()

    confirmed_count = appointments.filter(
        status="confirmed"
    ).count()

    completed_count = appointments.filter(
        status="completed"
    ).count()

    cancelled_count = appointments.filter(
        status="cancelled"
    ).count()

    return render(
        request,
        "owner/customers/detail.html",
        {
            "customer": customer,
            "appointments": appointments,
            "pending_count": pending_count,
            "confirmed_count": confirmed_count,
            "completed_count": completed_count,
            "cancelled_count": cancelled_count,
        },
    )
