from django.db import models

#
# Курсы
#

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

#
# Уроки
#

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

#
# Тесты к урокам
#

class Test(models.Model):
    lesson = models.ForeignKey(  # Меняем на ForeignKey для нескольких тестов к уроку
        'Lesson',
        on_delete=models.CASCADE,
        related_name='tests',
        verbose_name='Урок',
        blank=True,
        null=True
    )
    title = models.CharField(max_length=200, verbose_name='Название теста')
    pass_score = models.PositiveIntegerField(
        default=80,
        verbose_name='Минимальный балл (%)'
    )
    is_required = models.BooleanField(default=True, verbose_name='Обязательный')

    def __str__(self):
        return f"{self.title} (урок: {self.lesson.title if self.lesson else 'без урока'})"

class Question(models.Model):
    QUESTION_TYPES = [
        ('SINGLE', 'Один правильный ответ'),
        ('MULTIPLE', 'Несколько правильных ответов'),
        ('TEXT', 'Текстовый ответ'),
    ]

    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField(verbose_name='Текст вопроса')
    type = models.CharField(
        max_length=10,
        choices=QUESTION_TYPES,
        default='SINGLE',
        verbose_name='Тип вопроса'
    )
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        ordering = ['order']

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=300, verbose_name='Вариант ответа')
    is_correct = models.BooleanField(default=False, verbose_name='Правильный?')

    def __str__(self):
        return f"{self.text} ({'✓' if self.is_correct else '✗'})"

class TextAnswer(models.Model):
    """Для хранения текстовых ответов пользователей"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    answer_text = models.TextField(verbose_name='Ответ пользователя')
    is_approved = models.BooleanField(
        default=False,
        verbose_name='Проверен инструктором'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('question', 'user')