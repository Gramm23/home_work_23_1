import random

from django.contrib.auth.models import AbstractUser
from django.db import models
from product.models import NULLABLE

code = ''.join([str(random.randint(0, 9)) for _ in range(9)])


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')
    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    country = models.CharField(max_length=50, verbose_name='страна', **NULLABLE)
    email_verified = models.BooleanField(default=False, verbose_name='Верификация почты')

    ver_code = models.CharField(max_length=15, default=code, verbose_name='проверочный код', **NULLABLE)
    is_active = models.BooleanField(default=False, verbose_name='Активность')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email} {self.is_active}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
