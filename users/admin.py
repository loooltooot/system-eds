from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

from .models import User

# Register your models here.

@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    model = User
    fieldsets = [
        ('Личная информация', {
            'fields': ['surname', 'name', 'patronymic', 'phone', 'email', 'photo', 'students_unit']
        }),
        ('Уровень доступа', {
            'fields': ['groups', 'is_superuser', 'is_staff']
        }),
        ('Техническая информация', {
            'fields': ['password', 'is_active', 'date_joined', 'last_login']
        })
    ]
    add_fieldsets = [
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('surname', 'name', 'patronymic', 'groups', 'phone', 'password1', 'password2'),
            },
        ),
    ]
    list_display = ('surname', 'name', 'patronymic', 'phone', 'email', 'students_unit')
    list_display_links = ('phone', 'surname',)
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('phone', 'surname', 'name', 'patronymic', 'students_unit')
    ordering = ('surname',)