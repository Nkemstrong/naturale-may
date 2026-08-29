from urllib.parse import quote

from django.conf import settings
from django.shortcuts import get_object_or_404, render

from .models import Product


def shop(request):
    products = Product.objects.filter(
        is_active=True
    ).select_related("category")

    return render(
        request,
        "products/shop.html",
        {
            "products": products,
        }
    )


def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.prefetch_related("images"),
        slug=slug,
        is_active=True,
    )

    whatsapp_number = settings.NATURALE_MAY_WHATSAPP

    message = (
        f"Hello Naturale May, I would like to order {product.name}. "
        f"The listed price is ₦{product.price:,.2f}. "
        f"Please let me know how I can proceed with my order."
    )

    whatsapp_url = (
        f"https://wa.me/{whatsapp_number}"
        f"?text={quote(message)}"
    )

    return render(
        request,
        "products/detail.html",
        {
            "product": product,
            "whatsapp_url": whatsapp_url,
        }
    )