from typing import Any
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core import mail
from django.test import TestCase
from django.test.client import BOUNDARY, MULTIPART_CONTENT, encode_multipart
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from faker import Faker
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from app.user.models import Profile
from app.user.token import account_activation_token

from .mocks import test_image, test_user

User = get_user_model()
fake = Faker()


class UserRegisterViewsTest(TestCase):
    """
    Test case for user registration views
    """

    user: Any

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = User.objects.create_user(
            fake.name(), fake.email(), fake.password()
        )

    def setUp(self) -> None:
        self.create_url = reverse("register")

    def test_create_user(self) -> None:
        """
        Test can create user
        """
        data = {
            "username": fake.name(),
            "email": fake.email(),
            "password": fake.password(),
        }

        response = self.client.post(self.create_url, data, format="json")
        res_data = response.data  # type: ignore[attr-defined]

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res_data["username"], data["username"])
        self.assertEqual(res_data["email"], data["email"])
        self.assertTrue(len(mail.outbox) > 0)

    def test_new_user_verification(self) -> None:
        """
        Test verification of user
        """
        link = reverse(
            "email-verify",
            kwargs={
                "uidb64": urlsafe_base64_encode(force_bytes(self.user.pk)),
                "token": account_activation_token.make_token(self.user),
            },
        )

        resp = self.client.patch(link)

        self.assertEqual(resp.status_code, 200)

    def test_invalid_user_id(self) -> None:
        """
        Test invalid user id
        """
        link = reverse(
            "email-verify",
            kwargs={
                "uidb64": urlsafe_base64_encode(force_bytes("300")),
                "token": account_activation_token.make_token(self.user),
            },
        )

        resp = self.client.patch(link)

        self.assertEqual(resp.status_code, 400)
        self.assertIn("Invalid user id", str(resp.data))  # type: ignore[attr-defined]

    def test_invalid_token(self) -> None:
        """
        Test cannot use invalid token
        """
        link = reverse(
            "email-verify",
            kwargs={
                "uidb64": urlsafe_base64_encode(force_bytes(self.user.pk)),
                "token": "rgtuj54647vhd",
            },
        )

        resp = self.client.patch(link)

        self.assertEqual(resp.status_code, 400)
        self.assertIn("Invalid or expired token", str(resp.data))  # type: ignore[attr-defined]


class TestProfileView(APITestCase):
    def setUp(self) -> None:
        self.user_test = User.objects.create_user(**test_user)

        self.client = APIClient()

    @property
    def bearer_token(self) -> str:
        login_url = reverse("login")
        response = self.client.post(
            login_url,
            data={
                "email": test_user["email"],
                "password": test_user["password"],
            },
            format="json",
        )
        return response.data.get("access")  # type: ignore[no-any-return]

    @patch(
        "cloudinary.uploader.upload_resource", return_value=fake.image_url()
    )
    def test_profile_update(self, upload_resource: Any) -> None:
        Profile.objects.create(user=self.user_test)
        data = {
            "bio": "Do I function",
            "image": test_image,
        }
        url = reverse("profile", kwargs={"user": self.user_test.id})
        self.client.defaults[
            "HTTP_AUTHORIZATION"
        ] = f"Bearer {self.bearer_token}"
        response = self.client.patch(
            url,
            data=encode_multipart(data=data, boundary=BOUNDARY),
            content_type=MULTIPART_CONTENT,
            enctype="multipart/form-data",
        )

        self.assertTrue(upload_resource.called)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestPasswordReset(TestCase):
    testuser: dict
    user: Any

    @classmethod
    def setUpClass(cls) -> None:
        cls.testuser = {
            "username": fake.user_name(),
            "email": fake.email(),
            "password": fake.password(),
        }
        cls.user = User.objects.create_user(**cls.testuser)
        return super().setUpClass()

    def test_password_reset_request(self) -> None:
        url = reverse("password-reset")
        data = {"email": self.testuser["email"]}
        outbox = len(mail.outbox)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), outbox + 1)

    def test_password_reset_none_existing_email(self) -> None:
        url = reverse("password-reset")
        data = {"email": fake.email()}
        outbox = len(mail.outbox)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), outbox + 0)

    def test_password_reset_no_email(self) -> None:
        url = reverse("password-reset")
        response = self.client.post(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "This field may not be null", str(response.data["email"])  # type: ignore[attr-defined]
        )

    def test_verify_password_reset_token(self) -> None:
        token = PasswordResetTokenGenerator().make_token(self.user)
        encoded_pk = urlsafe_base64_encode(force_bytes(self.user.pk))
        reset_url = reverse(
            "verify-password-reset",
            kwargs={"encoded_pk": encoded_pk, "token": token},
        )
        response = self.client.post(
            reset_url, data={"password": fake.password()}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_verify_password_reset_wrong_token(self) -> None:
        encoded_pk = urlsafe_base64_encode(force_bytes(self.user.pk))
        reset_url = reverse(
            "verify-password-reset",
            kwargs={"encoded_pk": encoded_pk, "token": "token"},
        )

        response = self.client.post(
            reset_url, data={"password": fake.password()}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "The reset token is invalid", str(response.data)  # type: ignore[attr-defined]
        )

    def test_verify_password_reset_wrong_encoded_pk(self) -> None:
        reset_url = reverse(
            "verify-password-reset",
            kwargs={"encoded_pk": "encoded_pk", "token": "token"},
        )

        response = self.client.post(
            reset_url, data={"password": fake.password()}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "The encoded_pk is invalid", str(response.data)  # type: ignore[attr-defined]
        )

    def test_invalid_user_id(self) -> None:

        reset_url = reverse(
            "verify-password-reset",
            kwargs={
                "encoded_pk": "encoded_pk",
                "token": "token",
            },
        )

        resp = self.client.post(reset_url)
        self.assertEqual(resp.status_code, 400)
        self.assertIn("This field is required", str(resp.data))  # type: ignore[attr-defined]
