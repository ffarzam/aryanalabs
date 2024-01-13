from abc import ABC, abstractmethod

import jwt

from django.contrib.auth.backends import ModelBackend
from django.core.cache import caches
from rest_framework.authentication import BaseAuthentication

from .models import CustomUser
from .utils import decode_jwt
from imdb import custom_exception


class AbstractTokenAuthentication(ABC, BaseAuthentication):

    @abstractmethod
    def authenticate(self, request):
        ...

    @staticmethod
    def get_payload(token):
        payload = decode_jwt(token)
        return payload

    @staticmethod
    def get_user_from_payload(payload):
        user_id = payload.get('user_id')
        try:
            user = CustomUser.objects.get(id=user_id)
        except:
            raise custom_exception.UserNotFound

        if not user.is_active:
            raise custom_exception.NotActiveUserError

        return user

    @staticmethod
    def validate_jti_token(payload):
        jti = payload.get('jti')
        user_id = payload.get('user_id')
        if not caches['auth'].keys(f"user_{user_id} || {jti}"):
            raise custom_exception.InvalidTokenError


class AccessTokenAuthentication(AbstractTokenAuthentication):
    authentication_header_prefix = 'Token'
    authentication_header_name = 'Authorization'

    def authenticate(self, request):

        authorization_header = self.get_authorization_header(request)

        self.check_prefix_exists(authorization_header)

        access_token = self.get_access_token(authorization_header)

        try:
            payload = self.get_payload(access_token)
        except jwt.ExpiredSignatureError:
            raise custom_exception.ExpiredAccessTokenError
        except Exception as e:
            raise custom_exception.CommonError(str(e))

        self.validate_jti_token(payload)

        user = self.get_user_from_payload(payload)

        return user, payload

    def get_authorization_header(self, request):
        authorization_header = request.headers.get(self.authentication_header_name)
        if not authorization_header:
            raise custom_exception.AuthorizationHeaderError
        return authorization_header

    def check_prefix_exists(self, authorization_header):
        prefix = authorization_header.split(' ')[0]
        if prefix != self.authentication_header_prefix:
            raise custom_exception.NotFoundPrefix

    @staticmethod
    def get_access_token(authorization_header):
        access_token = authorization_header.split(' ')[1]
        if access_token:
            return access_token
        raise custom_exception.NotFoundAccessToken


class RefreshTokenAuthentication(AbstractTokenAuthentication):

    def authenticate(self, request):
        refresh_token = request.data.get("refresh_token")

        try:
            payload = self.get_payload(refresh_token)
        except jwt.ExpiredSignatureError:
            raise custom_exception.ExpiredRefreshTokenError
        except Exception as e:
            raise custom_exception.CommonError(str(e))

        self.validate_jti_token(payload)

        user = self.get_user_from_payload(payload)

        return user, payload



class AuthBackend(ModelBackend):

    def authenticate(self, request, user_identifier=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(username=user_identifier)
        except CustomUser.DoesNotExist:
            try:
                user = CustomUser.objects.get(email=user_identifier)
            except CustomUser.DoesNotExist:
                return None

        if user.check_password(password):
            return user
        else:
            return None

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None
