from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Расширенная модель пользователя с ролями и доступом к курсам.
    Теперь пользователи НЕ записываются на курсы, а получают доступ.
    """
    ROLE_CHOICES = [
        ('TRAINEE', 'Стажер'),  # Может просматривать только базовые курсы
        ('MASTER', 'Мастер'),   # Доступ к продвинутым курсам
        ('INSTRUCTOR', 'Инструктор'),  # Может редактировать курсы
    ]

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='TRAINEE',
        verbose_name='Роль в системе'
    )
    phone = models.CharField(
        max_length=15,
        blank=True,
        verbose_name='Контактный телефон'
    )
    available_courses = models.ManyToManyField(
        'courses.Course',
        verbose_name='Доступные курсы',
        blank=True,
        help_text='Курсы, которые видит пользователь в своем кабинете'
    )