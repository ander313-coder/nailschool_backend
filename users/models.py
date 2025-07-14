from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.core.validators import RegexValidator


class User(AbstractUser):
    ROLE_CHOICES = [
        ('TRAINEE', 'Стажёр'),
        ('MASTER', 'Мастер'),
        ('TOP_MASTER', 'Топ-мастер'),
        ('INSTRUCTOR', 'Инструктор'),
        ('STUDENT', 'Ученик'),
    ]

    # Убираем стандартное поле username
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')

    # Добавляем related_name для групп и прав
    groups = models.ManyToManyField(
        Group,
        verbose_name='Группы',
        blank=True,
        related_name='custom_user_set',
        related_query_name='user'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='Права пользователя',
        blank=True,
        related_name='custom_user_set',
        related_query_name='user'
    )

    phone = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$')],
        verbose_name='Телефон'
    )
    first_name = models.CharField(max_length=30, verbose_name='Имя')
    last_name = models.CharField(max_length=30, verbose_name='Фамилия')
    role = models.CharField(
        max_length=11,
        choices=ROLE_CHOICES,
        default='TRAINEE',
        verbose_name='Роль'
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name='Аватар'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'phone']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-created_at']