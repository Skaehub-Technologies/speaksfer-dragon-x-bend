from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Profile, FollowUnfollow

from app.user.serializers import ( UserSerializer, 
        VerifyEmailSerializer,
        FollowUnfollowSerializer,
        ProfileSerializer,
        FollowUnfollowSerializerSorted,
)

User = get_user_model()
class UserRegister(APIView):
    def post(self, request: Request, format: str = "json") -> Response:
        serializer = UserSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        response = serializer.data
        response["refresh"] = str(refresh)
        response["access"] = str(refresh.access_token)

        return Response(response, status=status.HTTP_201_CREATED)
class VerifyEmailView(GenericAPIView):
    serializer_class = VerifyEmailSerializer

    def patch(
        self, request: Request, uidb64: str, token: str, **kwargs: str
    ) -> Response:
        data = {"uidb64": uidb64, "token": token}

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("Email verified", status=status.HTTP_200_OK)

class ProfileDetails(APIView):
    def get(self, request):
        profile = Profile.objects.all()
        serializer = ProfileSerializer(profile, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response("Profile successfully created")

class ViewsProfile(APIView):
    def get(self, request, pk):
        profile = Profile.objects.get(id=pk)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
class FollowProfile(APIView):
    def post(self, request, user_pk):
        check_follow = FollowUnfollow.objects.filter(user_id=user_pk, follow_status='follow')
        if not check_follow:
            serializer = FollowUnfollowSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
            return Response("Successfully followed")
        else:
            return Response("You are already following the user")
class UnFollowProfile(APIView):
    def post(self, request, user_pk):
        check_follow = FollowUnfollow.objects.filter(user_id=user_pk ,follow_status='follow')
        if check_follow:
            check_follow.delete()
            return Response("Successfully unfollowed")
        else:
            return Response("You haven't followed anyone yet")
class ViewFollowers(APIView):
    def get(self, request, pk):
        fetch_profile = FollowUnfollow.objects.filter(profile=pk, follow_status='follow')
        if fetch_profile:
            serializer = FollowUnfollowSerializerSorted(fetch_profile, many=True)
            return Response(serializer.data)
        else:
            return Response("You don't have followers")
class ViewFollowings(APIView):
    def get(self, request, pk):
        fetch_user = User.objects.get(id=pk)
        following_user = fetch_user.followunfollow_set.all()
        serializer = FollowUnfollowSerializerSorted(following_user, many=True)
        return Response(serializer.data)