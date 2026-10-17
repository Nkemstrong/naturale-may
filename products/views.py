from owner.models import BusinessSettings

from decimal import Decimal

from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from core.whatsapp import whatsapp_url
from .models import Order, OrderItem, Product


def shop(request):
    products = (
        Product.objects
        .filter(is_active=True)
        .select_related("category")
        .prefetch_related("images")
    )

    return render(
        request,
        "products/shop.html",
        {
            "products": products,
        },
    )


def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects
        .select_related("category")
        .prefetch_related("images"),
        slug=slug,
        is_active=True,
    )

    message = (
        f"Hello Naturale May, I would like to order {product.name}. "
        f"The listed price is ₦{product.price:,.2f}. "
        "Please let me know how I can proceed with my order."
    )

    return render(
        request,
        "products/detail.html",
        {
            "product": product,
            "whatsapp_url": whatsapp_url(message) or "#",
        },
    )


def cart(request):
    """
    Display the customer's current shopping cart.

    The cart is stored in the Django session.
    """

    cart_data = request.session.get("cart", {})

    cart_items = []
    total = Decimal("0.00")

    for product_id, quantity in cart_data.items():

        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            continue

        if quantity < 1:
            continue

        product = (
            Product.objects
            .filter(
                id=product_id,
                is_active=True,
                stock_status="in_stock",
            )
            .select_related("category")
            .first()
        )

        if not product:
            continue

        subtotal = product.price * quantity
        total += subtotal

        cart_items.append(
            {
                "product": product,
                "quantity": quantity,
                "subtotal": subtotal,
            }
        )

    return render(
        request,
        "products/cart.html",
        {
            "cart_items": cart_items,
            "cart_total": total,
        },
    )


def add_to_cart(request, product_id):
    """
    Add a product to the session cart.
    """

    if request.method != "POST":
        return redirect("products:shop")

    product = get_object_or_404(
        Product,
        id=product_id,
        is_active=True,
    )

    if product.stock_status != "in_stock":
        messages.error(
            request,
            f"{product.name} is currently not available.",
        )
        return redirect("products:shop")

    try:
        quantity = int(
            request.POST.get("quantity", 1)
        )
    except (TypeError, ValueError):
        quantity = 1

    if quantity < 1:
        quantity = 1

    cart_data = request.session.get(
        "cart",
        {},
    )

    product_key = str(product.id)

    current_quantity = int(
        cart_data.get(product_key, 0)
    )

    cart_data[product_key] = (
        current_quantity + quantity
    )

    request.session["cart"] = cart_data
    request.session.modified = True

    messages.success(
        request,
        f"{product.name} has been added to your cart.",
    )

    return redirect("products:cart")


def update_cart(request):
    """
    Update the quantity of a product in the cart.

    The product ID is submitted through POST.
    """

    if request.method != "POST":
        return redirect("products:cart")

    product_id = request.POST.get("product_id")

    if not product_id:
        messages.error(
            request,
            "Unable to update the cart item.",
        )
        return redirect("products:cart")

    try:
        product_id = int(product_id)
    except (TypeError, ValueError):
        messages.error(
            request,
            "Invalid product.",
        )
        return redirect("products:cart")

    product = get_object_or_404(
        Product,
        id=product_id,
        is_active=True,
    )

    try:
        quantity = int(
            request.POST.get("quantity", 1)
        )
    except (TypeError, ValueError):
        quantity = 1

    cart_data = request.session.get(
        "cart",
        {},
    )

    product_key = str(product.id)

    if quantity <= 0:
        cart_data.pop(
            product_key,
            None,
        )

        messages.success(
            request,
            f"{product.name} was removed from your cart.",
        )
    else:
        cart_data[product_key] = quantity

        messages.success(
            request,
            f"{product.name} quantity updated.",
        )

    request.session["cart"] = cart_data
    request.session.modified = True

    return redirect("products:cart")


def remove_from_cart(request, product_id):
    """
    Remove a product completely from the cart.
    """

    if request.method != "POST":
        return redirect("products:cart")

    cart_data = request.session.get(
        "cart",
        {},
    )

    cart_data.pop(
        str(product_id),
        None,
    )

    request.session["cart"] = cart_data
    request.session.modified = True

    return redirect("products:cart")


def checkout(request):
    """
    Collect customer information and create an order.
    """

    cart_data = request.session.get(
        "cart",
        {},
    )

    if not cart_data:
        messages.warning(
            request,
            "Your cart is empty.",
        )
        return redirect("products:shop")

    cart_items = []
    total = Decimal("0.00")

    for product_id, quantity in cart_data.items():

        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            continue

        if quantity < 1:
            continue

        product = (
            Product.objects
            .filter(
                id=product_id,
                is_active=True,
                stock_status="in_stock",
            )
            .first()
        )

        if not product:
            continue

        subtotal = product.price * quantity
        total += subtotal

        cart_items.append(
            {
                "product": product,
                "quantity": quantity,
                "subtotal": subtotal,
            }
        )

    if not cart_items:
        request.session["cart"] = {}
        request.session.modified = True

        messages.warning(
            request,
            "The products in your cart are no longer available.",
        )

        return redirect("products:shop")

    if request.method == "POST":

        customer_name = request.POST.get(
            "customer_name",
            "",
        ).strip()

        customer_email = request.POST.get(
            "customer_email",
            "",
        ).strip()

        customer_phone = request.POST.get(
            "customer_phone",
            "",
        ).strip()

        delivery_address = request.POST.get(
            "delivery_address",
            "",
        ).strip()

        if not all(
            [
                customer_name,
                customer_email,
                customer_phone,
                delivery_address,
            ]
        ):
            messages.error(
                request,
                "Please complete all customer and delivery details.",
            )

            return render(
                request,
                "products/checkout.html",
                {
                    "cart_items": cart_items,
                    "cart_total": total,
                    "form_data": request.POST,
                },
            )

        with transaction.atomic():

            order = Order.objects.create(
                customer_name=customer_name,
                customer_email=customer_email,
                customer_phone=customer_phone,
                delivery_address=delivery_address,
                total_amount=total,
                payment_status="pending",
                order_status="pending",
            )

            for item in cart_items:

                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    quantity=item["quantity"],
                    price=item["product"].price,
                    subtotal=item["subtotal"],
                )

        request.session["cart"] = {}
        request.session.modified = True

        return redirect(
            "products:payment",
            order_number=order.order_number,
        )

    return render(
        request,
        "products/checkout.html",
        {
            "cart_items": cart_items,
            "cart_total": total,
        },
    )


def payment(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    # Business settings drive the bank details shown on this page.
    business_settings = BusinessSettings.objects.filter(pk=1).first()

    items_text = "\n".join(
        f"- {item.product.name} x{item.quantity} "
        f"(₦{item.subtotal:,.2f})"
        for item in order.items.all()
    )

    message = (
        f"Hello Naturale May,\n\n"
        f"I have placed an order and made payment.\n\n"
        f"Order Number: {order.order_number}\n"
        f"Name: {order.customer_name}\n"
        f"Phone: {order.customer_phone}\n"
        f"Email: {order.customer_email}\n"
        f"Delivery Address: {order.delivery_address}\n\n"
        f"Items:\n{items_text}\n\n"
        f"Total: ₦{order.total_amount:,.2f}\n\n"
        f"I will attach my payment receipt here for verification."
    )

    return render(
        request,
        "products/payment.html",
        {
            "order": order,
            "business_settings": business_settings,
            "whatsapp_url": whatsapp_url(message),
        },
    )