from django.contrib.auth.backends import ModelBackend

from .models import CustomUser


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
