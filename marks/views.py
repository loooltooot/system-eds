from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render

from .models import Appointment
from .mixins import AdminRedirectMixin

# Create your views here.

class IndexView(LoginRequiredMixin, AdminRedirectMixin, View):
    def get(self, request, *args, **kwargs):
        template = 'marks/dashboard/student.html'
        context = {'related_appointments': Appointment.objects.filter(students_unit=request.user.students_unit)}

        if request.user.groups.filter(name='Преподаватели').exists():
            template = 'marks/dashboard/teacher.html'
            context['related_appointments'] = Appointment.objects.filter(teacher=request.user)

        return render(request, template, context)
    
class AddMarkView(LoginRequiredMixin, PermissionRequiredMixin, AdminRedirectMixin, View):
    permission_required = 'marks.add_mark'

    def get(self, request, *args, **kwargs):
        template = 'marks/addmark.html'
        
    def post(self, request, *args, **kwargs):
        pass