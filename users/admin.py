from django.contrib import admin
from django import forms
from .models import User

class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not phone.startswith('+'):
            raise forms.ValidationError("Номер должен начинаться с '+'")
        if len(phone) < 12:
            raise forms.ValidationError("Слишком короткий номер")
        return phone

    def clean(self):
        # Проверка для инструкторов
        if self.cleaned_data.get('role') == 'INSTRUCTOR' and not self.cleaned_data.get('is_staff'):
            raise forms.ValidationError("Инструктор должен иметь права staff")

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm  # Подключаем нашу валидацию
    list_display = ('email', 'phone', 'first_name', 'last_name', 'role', 'created_at')
    list_filter = ('role', 'created_at')
    search_fields = ('email', 'phone', 'first_name')
    readonly_fields = ('created_at',)

    fieldsets = (
        ('Основное', {
            'fields': ('email', 'phone', 'first_name', 'last_name')
        }),
        ('Права', {
            'fields': ('role', 'is_active', 'is_staff')
        }),
        ('Дополнительно', {
            'fields': ('avatar', 'created_at')
        }),
    )