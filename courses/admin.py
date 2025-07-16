from django.contrib import admin
from .models import Course, Lesson, LessonFile

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

admin.site.register(Course)
admin.site.register(LessonFile)