import os
os.environ["DJANGO_TEST"] = "True"

from urllib import response

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


class OwnerAccessTests(TestCase):
    def test_public_pages_are_available_to_anonymous_customers(self):
        public_urls = [
            reverse("core:home"),
            reverse("core:about"),
            reverse("products:shop"),
            reverse("services:list"),
            reverse("appointments:book"),
            reverse("contact:contact"),
        ]

        for url in public_urls:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)

    def test_dashboard_requires_owner_login(self):
        response = self.client.get(reverse("owner:dashboard"))

        self.assertRedirects(
            response,
            f"{reverse('owner:login')}?next={reverse('owner:dashboard')}",
        )

    def test_dashboard_rejects_authenticated_non_staff_users(self):
        user = get_user_model().objects.create_user(
            username="customer",
            password="test-password",
        )
        self.client.force_login(user)

        response = self.client.get(reverse("owner:dashboard"))

        self.assertRedirects(
            response,
            f"{reverse('owner:login')}?next={reverse('owner:dashboard')}",
        )

    def test_dashboard_is_available_to_staff_users(self):
        user = get_user_model().objects.create_user(
            username="owner",
            password="test-password",
            is_staff=True,
        )
        self.client.force_login(user)

        response = self.client.get(reverse("owner:dashboard"))

        self.assertEqual(response.status_code, 200)

    def test_owner_login_is_available_at_dashboard_login(self):
        response = self.client.get(reverse("owner:login"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'class="auth-page"')
        self.assertContains(response, "/static/css/style.")
        self.assertContains(response, ".css")

    def test_owner_login_accepts_staff_credentials(self):
        get_user_model().objects.create_user(
            username="owner",
            password="test-password",
            is_staff=True,
        )

        response = self.client.post(
            reverse("owner:login"),
            {"username": "owner", "password": "test-password"},
        )

        self.assertRedirects(response, reverse("owner:dashboard"))

    def test_admin_and_generic_account_login_urls_are_not_public(self):
        self.assertEqual(self.client.get("/admin/").status_code, 404)
        self.assertEqual(self.client.get("/accounts/login/").status_code, 404)
