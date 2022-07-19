from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from app.user.views import UserRegister, VerifyEmailView

from . import views


urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", UserRegister.as_view(), name="register"),
    path(
        "email-verify/<str:uidb64>/<str:token>/",
        VerifyEmailView.as_view(),
        name="email-verify",
    ),
    path('profile_details/', views.ProfileDetails.as_view(), name='add_profile_details'),
    path('show_profile/<str:pk>/', views.ViewsProfile.as_view(), name="view_profile"),
    path('follow_profile/<str:user_pk>/', views.FollowProfile.as_view(), name="follow_profile"),
    path('unfollow_profile/<str:user_pk>/', views.UnFollowProfile.as_view(), name="unfollow_profile"),
    path('view_followers/<str:pk>/', views.ViewFollowers.as_view(), name="view_followers"),
    path('view_followings/<str:pk>/', views.ViewFollowings.as_view(), name="view_followings"),
]
