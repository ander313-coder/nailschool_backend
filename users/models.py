from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    # Указываем уникальные related_name
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        related_name='custom_user_set',  # Уникальное имя
        related_query_name='user'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='custom_user_set',  # Уникальное имя
        related_query_name='user'
    )

    # Наши кастомные поля
    ROLE_CHOICES = [
        ('MASTER', 'Мастер'),
        ('INSTRUCTOR', 'Инструктор'),
    ]
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='MASTER'
    )
    phone = models.CharField(max_length=15, blank=True)

    class Meta:
        # Убедитесь, что в settings.py указано AUTH_USER_MODEL = 'users.User'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username