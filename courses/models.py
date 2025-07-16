from django.db import models

class Course(models.Model):
    """
    Модель курса с обязательными видеоуроками и тестами.
    Доступ регулируется через поле `access_level`.
    """
    ACCESS_LEVELS = [
        ('BASIC', 'Для стажеров'),
        ('ADVANCED', 'Для мастеров'),
        ('ALL', 'Для всех'),
    ]

    title = models.CharField(
        max_length=200,
        verbose_name='Название курса'
    )
    description = models.TextField(
        verbose_name='Описание',
        help_text='Форматированное описание курса (можно использовать HTML)'
    )
    access_level = models.CharField(
        max_length=10,
        choices=ACCESS_LEVELS,
        default='BASIC',
        verbose_name='Уровень доступа'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    def __str__(self):
        return f"{self.title} ({self.get_access_level_display()})"

class Lesson(models.Model):
    """
    Урок в составе курса. Содержит видео, материалы и тесты.
    """
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name='Родительский курс'
    )
    title = models.CharField(
        max_length=200,
        verbose_name='Название урока'
    )
    video_url = models.URLField(
        blank=True,
        null=True,
        verbose_name='Ссылка на видео',
        help_text='Ссылка на YouTube или собственный видеохостинг'
    )
    materials = models.FileField(
        upload_to='course_materials/',
        blank=True,
        null=True,
        verbose_name='Дополнительные материалы'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядковый номер',
        help_text='Уроки сортируются по этому полю'
    )

    class Meta:
        ordering = ['order']  # Автоматическая сортировка уроков

    def __str__(self):
        return f"{self.course.title} - Урок {self.order}: {self.title}"

class LessonFile(models.Model):
    """Модель для множественных файлов урока"""
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='lesson_files/')
    title = models.CharField(max_length=100, blank=True, verbose_name='Название файла')

    def __str__(self):
        return self.title or f"Файл {self.id}"