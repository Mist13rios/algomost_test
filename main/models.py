from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
# Create your models here.


class ShowcaseItem(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=None)
    available = models.BooleanField(default=True)


class Specializations(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "specializations"


class UserPoll(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    specialization = models.ForeignKey(Specializations, on_delete=models.DO_NOTHING)
    mail = models.EmailField(null=True)
    side_acc = models.URLField(null=True)


class OrderCart(models.Model):
    items = models.ForeignKey(ShowcaseItem, on_delete=models.DO_NOTHING)


class AppUser(AbstractUser):

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = "App Users"


class AppUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, username, full_name, password, **extra_fields):
        """
        Create and save a user with the given username, email,
        full_name, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        if not username:
            raise ValueError('The given username must be set')
        if not full_name:
            raise ValueError('The given full name must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(
            email=email, username=username, full_name=full_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username, full_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(
            email, username, full_name, password, **extra_fields
        )

    def create_superuser(self, email, username, full_name, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(
            email, username, full_name, password, **extra_fields
        )
