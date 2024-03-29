from django.contrib.auth.models import BaseUserManager
from django.db.models import QuerySet


class AppQuerySet(QuerySet):
    def delete(self):
        self.update(is_deleted=True)


class CustomManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

    def create_user(self, email, username, password):
        if not email:
            raise ValueError("Users must have an email")
        if not username:
            raise ValueError("Users must have an username")

        user = self.model(username=username, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(email, username, password)
        user.is_account_enable = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
