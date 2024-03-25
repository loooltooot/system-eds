from django.contrib import admin
from django.contrib.auth import get_user_model
from django.http import HttpRequest

from .models import (
    Mark, Subject, StudentsUnit, Appointment
)

# Register your models here.

@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display = ['value', 'subject', 'teacher', 'student', 'student_unit', 'pub_date']
    search_fields = [
        'subject__name', 'student__students_unit__name', 'student__surname', 'student__name', 'student__patronymic',
        'teacher__surname', 'teacher__name', 'teacher__patronymic',
    ]
    ordering = ['-pub_date']

    @admin.display(description='группа')
    def student_unit(self, obj):
        return f'{obj.student.students_unit}'

class AppointmentInline(admin.TabularInline):
    model = Appointment
    extra = 0
    classes = ['collapse']

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name', 'description']
    inlines = [AppointmentInline]

class StudentsInline(admin.TabularInline):
    model = get_user_model()
    fields = ['surname', 'name', 'patronymic', 'phone']
    extra = 0
    show_change_link = True
    verbose_name = 'студент'
    verbose_name_plural = 'студенты'
    classes = ['collapse']
    can_delete = False

    def has_add_permission(self, *args) -> bool:
        return False
    
    def has_change_permission(self, *args) -> bool:
        return False

@admin.register(StudentsUnit)
class StudentsUnitAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'students_count']
    search_fields = ['name', 'description']
    inlines = [StudentsInline]

    @admin.display(description='кол-во студентов')
    def students_count(self, obj):
        return f'{obj.user_set.count()}'

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['students_unit', 'subject', 'teacher', 'pub_date']
    list_display_links = ['students_unit', 'pub_date']
    search_fields = [
        'subject__name', 'students_unit__name', 'teacher__surname', 'teacher__name', 'teacher__patronymic',
    ]
    ordering = ['-pub_date']