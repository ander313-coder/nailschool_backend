from django.contrib import admin
from .models import Course, Lesson

class LessonInline(admin.TabularInline):
    """Редактирование уроков прямо в интерфейсе курса"""
    model = Lesson
    extra = 1  # Количество пустых форм для добавления
    fields = ('title', 'video_url', 'materials', 'order')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Настройка отображения курсов в админке"""
    list_display = ('title', 'access_level', 'created_at')
    list_filter = ('access_level',)
    search_fields = ('title', 'description')
    inlines = [LessonInline]  # Добавляем уроки к курсу

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """Управление уроками"""
    list_display = ('title', 'course', 'order')
    list_editable = ('order',)  # Быстрое редактирование порядка