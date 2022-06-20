from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from app.user.serializers import UserSerializer, UserTokenObtainPairSerializer


class UserRegister(APIView):
    def post(self, request, format="json"):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        response = serializer.data
        response["refresh"] = str(refresh)
        response["access"] = str(refresh.access_token)

        return Response(response, status=status.HTTP_201_CREATED)


class UserTokenObtainPairView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer
