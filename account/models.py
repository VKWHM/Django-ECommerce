from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.core.mail import send_mail
from django.db import models
from django_countries.fields import CountryField


class CustomUserManager(BaseUserManager):
    def create_superuser(self, email, username, password, **kwargs):
        kwargs.setdefault('is_active', True)
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        for field in ['is_staff', 'is_superuser']:
            if not kwargs.get(field, False):
                raise ValueError(f"Superuser must be assigned to {field}=True")

        self.create_user(email, username, password, **kwargs)

    def create_user(self, email, username, password, **kwargs):
        if not email:
            raise ValueError("You must provide an email address")
        n_email = self.normalize_email(email)
        user = self.model(email=n_email, username=username, **kwargs)
        user.set_password(password)
        user.save()
        return user



class UserBase(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("email address", unique=True)
    username_validator = ASCIIUsernameValidator()
    username = models.CharField("username", max_length=150, unique=True, validators=[username_validator], error_messages={'unique':'A user with that username already exists.'})
    first_name = models.CharField("first name", max_length=150, blank=True)
    about = models.TextField('about', max_length=500, blank=True)
    country = CountryField()
    phone_number = models.CharField(max_length=15, blank=True)
    postcode = models.CharField(max_length=12, blank=True)
    address_line_1 = models.CharField(max_length=150, blank=True)
    address_line_2 = models.CharField(max_length=150, blank=True)
    town_city = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField("active", default=True)
    is_staff = models.BooleanField("active", default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"

    def email_user(self, subject, message):
        send_mail(
            subject,
            message,
            'l@1.com',
            [self.email],
            fail_silently=False,
        )

    def __str__(self):
        return self.username
