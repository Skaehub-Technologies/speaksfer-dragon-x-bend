from typing import Any

from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from faker import Faker
from rest_framework import status

from app.user.token import account_activation_token

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

class TestUserFollowing(TestCase):
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

    # def test_wrong_user_follow(self) -> None:
    #     url = reverse(
    #         "follow_profile", kwargs={"user_pk": self.testuser}
    #     )
    #     response = self.client.post(url, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)    

    # def test_wrong_user_unfollow(self) -> None:
    #     url = reverse(
    #         "unfollow_profile", kwargs={"user_pk": self.testuser.get("user.id",2)}
    #     )
    #     response = self.client.delete(url, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) 

    def test_user_follow(self) -> None:
        url = reverse(
            "follow_profile", kwargs={"user_pk": self.testuser.get("user.id")}
        )
        import pdb; pdb.set_trace()
        response = self.client.post(
            url,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(
            "Successfully followed", str(response.data)  # type: ignore[attr-defined]
        )

    # def test_user_unfollow(self) -> None:
    #     self.client.post(
    #         reverse(
    #             "unfollow_profile/<str:user_pk>/", kwargs={"user_pk": self.testuser.user_pk}
    #         ),
    #         format="json",
    #     )
    #     url = reverse(
    #         "unfollow_profile/<str:user_pk>/", kwargs={"user_pk": self.testuser.user_pk}
    #     )
    #     response = self.client.delete(
    #         url,
    #         format="json",
    #     )
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertIn(
    #         "Successfully unfollowed", str(response.data)  # type: ignore[attr-defined]
    #     )

    # def test_get_user_followers(self) -> None:
    #     url = reverse(
    #         "view_followers/<str:pk>/", kwargs={"user_id": self.testuser.user_pk}
    #     )
    #     response = self.client.get(
    #         url,
    #         format="json",
    #     )
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertIn(
    #         "You don't have followers", str(response.data)  # type: ignore[attr-defined]
    #     )

    # def test_user_cannot_follow_same(self) -> None:
    #     url = reverse(
    #         "follow_profile/<str:user_pk>/", kwargs={"user_id": self.testuser.user_id}
    #     )
    #     response = self.client.post(
    #         url,
    #         format="json",
    #     )
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    #     self.assertIn(
    #         "You are already followed the user", str(response.data)  # type: ignore[attr-defined]
    #     )