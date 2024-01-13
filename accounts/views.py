from django.contrib.auth import authenticate
from django.core.cache import caches
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .authentication import AccessTokenAuthentication, RefreshTokenAuthentication
from .serializers import UserRegisterSerializer, UserLoginSerializer, UpdateUserSerializer
from .utils import set_token


# Create your views here.


class UserRegister(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserRegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.create(serializer.validated_data)

        return Response({'message': "Registered successfully",
                         "data": serializer.data},
                        status=status.HTTP_201_CREATED)


class UserLogin(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_identifier = serializer.validated_data.get('user_identifier')
        password = serializer.validated_data.get('password')
        user = authenticate(request, user_identifier=user_identifier, password=password)
        if user is None:
            return Response({'message': 'Invalid Username or Password'}, status=status.HTTP_400_BAD_REQUEST)
        elif not user.is_active:
            return Response({'message': "User is Banned"}, status=status.HTTP_404_NOT_FOUND)

        access_token, refresh_token = set_token(request, user, caches)
        data = {"access": access_token, "refresh": refresh_token}

        return Response({"message": "Logged in successfully", "data": data}, status=status.HTTP_201_CREATED)


class RefreshToken(APIView):
    authentication_classes = (RefreshTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        payload = request.auth

        jti = payload["jti"]
        caches['auth'].delete(f'user_{user.id} || {jti}')

        access_token, refresh_token = set_token(request, user, caches)
        data = {"access": access_token, "refresh": refresh_token}

        return Response(data, status=status.HTTP_201_CREATED)


class UpdateProfile(UpdateAPIView):
    http_method_names = ["patch"]
    authentication_classes = (AccessTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserSerializer

    def get_object(self):
        return self.request.user
