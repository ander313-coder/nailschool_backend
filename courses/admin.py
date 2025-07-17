from django.contrib import admin
from .models import Course, Lesson, LessonFile, TextAnswer, Question, Answer, Test


class LessonFileInline(admin.TabularInline):
    model = LessonFile
    extra = 1

class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    show_change_link = True

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    inlines = [LessonFileInline]
    list_display = ('title', 'course', 'has_video')
    list_filter = ('course',)

    def has_video(self, obj):
        return bool(obj.video_url)
    has_video.boolean = True
    has_video.short_description = 'Видео'

admin.site.register(Course)
admin.site.register(LessonFile)

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 2
    fields = ('text', 'is_correct', 'order')
    min_num = 1

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'test', 'type', 'order')
    list_editable = ('order',)
    list_filter = ('test', 'type')
    inlines = [AnswerInline]
    actions = ['change_to_single', 'change_to_multiple']

    @admin.action(description="Сделать вопросы с одним ответом")
    def change_to_single(self, request, queryset):
        queryset.update(type='SINGLE')

    @admin.action(description="Сделать вопросы с несколькими ответами")
    def change_to_multiple(self, request, queryset):
        queryset.update(type='MULTIPLE')

class TestInline(admin.StackedInline):
    model = Test
    extra = 0
    fields = ('title', 'pass_score', 'is_required')
    show_change_link = True

@admin.register(TextAnswer)
class TextAnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'user', 'is_approved', 'created_at')
    list_editable = ('is_approved',)
    search_fields = ('user__username', 'answer_text')
    list_filter = ('is_approved', 'question__test')