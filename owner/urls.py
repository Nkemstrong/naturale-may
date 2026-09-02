from django.urls import path

from . import views


app_name = "owner"


urlpatterns = [

    # ========================================================
    # AUTHENTICATION
    # ========================================================

    path(
        "login/",
        views.owner_login,
        name="login",
    ),

    path(
        "logout/",
        views.owner_logout,
        name="logout",
    ),

    path(
        "change-password/",
        views.change_password,
        name="change_password",
    ),


    # ========================================================
    # DASHBOARD
    # ========================================================

    path(
        "",
        views.dashboard,
        name="dashboard",
    ),
    
    path(
        "settings/",
        views.business_settings,
        name="business_settings",
    ),

    path(
        "appointments/<int:pk>/status/",
        views.update_appointment_status,
        name="appointment_status",
    ),


    # ========================================================
    # SERVICES
    # ========================================================

    path(
        "services/",
        views.services_list,
        name="services_list",
    ),

    path(
        "services/add/",
        views.service_create,
        name="service_create",
    ),

    path(
        "services/<int:pk>/edit/",
        views.service_edit,
        name="service_edit",
    ),

    path(
        "services/<int:pk>/toggle/",
        views.service_toggle,
        name="service_toggle",
    ),

    path(
        "services/<int:pk>/delete/",
        views.service_delete,
        name="service_delete",
    ),


    # ========================================================
    # PRODUCTS
    # ========================================================

    path(
        "products/",
        views.products_list,
        name="products_list",
    ),

    path(
        "products/add/",
        views.product_create,
        name="product_create",
    ),

    path(
        "products/<int:pk>/edit/",
        views.product_edit,
        name="product_edit",
    ),

    path(
        "products/<int:pk>/toggle/",
        views.product_toggle,
        name="product_toggle",
    ),

    path(
        "products/<int:pk>/feature/",
        views.product_feature_toggle,
        name="product_feature_toggle",
    ),

    path(
        "products/<int:pk>/delete/",
        views.product_delete,
        name="product_delete",
    ),


    # ========================================================
    # PRODUCT CATEGORIES
    # ========================================================

    path(
        "products/categories/",
        views.categories_list,
        name="categories_list",
    ),

    path(
        "products/categories/add/",
        views.category_create,
        name="category_create",
    ),

    path(
        "products/categories/<int:pk>/edit/",
        views.category_edit,
        name="category_edit",
    ),

    path(
        "products/categories/<int:pk>/toggle/",
        views.category_toggle,
        name="category_toggle",
    ),

    path(
        "products/categories/<int:pk>/delete/",
        views.category_delete,
        name="category_delete",
    ),


    # ========================================================
    # PRODUCT GALLERY
    # ========================================================

    path(
        "products/<int:pk>/gallery/",
        views.product_gallery,
        name="product_gallery",
    ),

    path(
        "products/<int:pk>/gallery/add/",
        views.product_image_create,
        name="product_image_create",
    ),

    path(
        "products/gallery/image/<int:pk>/edit/",
        views.product_image_edit,
        name="product_image_edit",
    ),

    path(
        "products/gallery/image/<int:pk>/delete/",
        views.product_image_delete,
        name="product_image_delete",
    ),


    # ========================================================
    # MESSAGES
    # ========================================================

    path(
        "messages/",
        views.messages_list,
        name="messages_list",
    ),

    path(
        "messages/<int:pk>/",
        views.message_detail,
        name="message_detail",
    ),

    path(
        "messages/<int:pk>/toggle-read/",
        views.message_toggle_read,
        name="message_toggle_read",
    ),

    path(
        "messages/<int:pk>/delete/",
        views.message_delete,
        name="message_delete",
    ),


    # ========================================================
    # CUSTOMERS
    # ========================================================

    path(
        "customers/",
        views.customers_list,
        name="customers_list",
    ),

    path(
        "customers/<int:pk>/",
        views.customer_detail,
        name="customer_detail",
    ),


    # ========================================================
    # ORDERS
    # ========================================================

    path(
        "orders/",
        views.orders_list,
        name="orders_list",
    ),

    path(
        "orders/<int:pk>/",
        views.order_detail,
        name="order_detail",
    ),

    path(
        "orders/<int:pk>/payment-status/",
        views.update_order_payment_status,
        name="update_order_payment_status",
    ),

    path(
        "orders/<int:pk>/status/",
        views.update_order_status,
        name="update_order_status",
    ),
]