import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model


class CustomUser(AbstractUser):
    USERNAME_FIELD = 'username'
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_num1 = models.CharField(max_length=25, default='+998941633015')
    phone_num2 = models.CharField(max_length=25, null=True)
    email = models.EmailField(default='zafarbekolimboyev07@gamil.com')
    createdAt = models.DateTimeField(default=datetime.datetime.now())
    updatedAt = models.DateTimeField(null=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = "Users"
        db_table = "users"


class PasswordResetModel(models.Model):
    user_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_time = models.DateTimeField(default=datetime.datetime.now())
    is_valid = models.BooleanField(default=True)
    reset_code = models.CharField(max_length=8)

    def __str__(self):
        return self.user_id

    class Meta:
        db_table = 'reset_codes'
        verbose_name_plural = 'reset_codes'
