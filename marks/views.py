from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect

from .models import Appointment

# Create your views here.

class IndexView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        template = 'marks/dashboard/student.html'
        context = {
            't_version': 'версия для студентов',
            'related_appointments': Appointment.objects.filter(students_unit=request.user.students_unit),
        }

        if request.user.groups.filter(name='Преподаватели').exists():
            template = 'marks/dashboard/teacher.html'
            context = {
                't_version': 'версия для преподавателей',
                'related_appointments': Appointment.objects.filter(teacher=request.user),
            }

        if (request.user.groups.filter(name='Администрация') and len(request.user.groups) == 1) or request.user.is_superuser:
            return redirect('admin/')

        return render(request, template, context)