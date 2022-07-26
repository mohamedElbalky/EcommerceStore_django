
from django_countries.fields import CountryField


from django.db import models

# translate the site to another languanges 
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


class CustomAccountManager(BaseUserManager):
    def create_user(self, email, username, password, **other_fields):
        if not email:
            raise ValueError(_("You must provide an email address"))
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **other_fields)
        user.set_password(password)
        user.save()
        return user
        
    def create_superuser(self, email, username, password, **other_fields):
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)

        if other_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must be assigned to is_staff=True"))

        if other_fields.get("is_superuser") is not True:
            raise ValueError(
                _("Superuser must be assigned to is_superuser=True"))

        if other_fields.get("is_active") is not True:
            raise ValueError(_("Superuser must be assigned to is_active=True"))

        return self.create_user(email, username, password, **other_fields)



class UserBase(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    about = models.TextField(_("about"), max_length=500, blank=True)

    # delivery details
    countery = CountryField()
    phone_number = models.CharField(max_length=15, blank=True)
    post_code = models.CharField(max_length=15, blank=True)
    adress_line_1 = models.CharField(max_length=150, blank=True)
    adress_line_2 = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CustomAccountManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "Accounts"
        verbose_name_plural = "Accounts"

    # def get_username(self):
    #     return str(self.username)

    def __str__(self):
        return self.username
