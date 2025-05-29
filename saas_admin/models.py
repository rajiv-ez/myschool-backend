from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import secrets

class SaaSAdminManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        return self.create_user(email, password, **extra_fields)

class InstitutionAdmin(AbstractBaseUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    objects = SaaSAdminManager()

    def __str__(self):
        return self.full_name

class InstitutionAdminToken(models.Model):
    key = models.CharField(max_length=40, primary_key=True, editable=False)
    user = models.OneToOneField(
        InstitutionAdmin,
        related_name='custom_auth_token',
        on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = secrets.token_hex(20)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.key
