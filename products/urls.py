from django.urls import path

from . import views


app_name = "products"


urlpatterns = [
    # Shop
    path("", views.shop, name="shop"),

    # Cart
    path("cart/", views.cart, name="cart"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/update/", views.update_cart, name="update_cart"),
    path("cart/remove/<int:product_id>/", views.remove_from_cart, name="remove_from_cart"),

    # Checkout & payment
    path("checkout/", views.checkout, name="checkout"),
    path("payment/<str:order_number>/", views.payment, name="payment"),

    # Product detail
    path("<slug:slug>/", views.product_detail, name="detail"),
]