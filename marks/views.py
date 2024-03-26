from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404

from .models import Appointment, StudentsUnit, Subject
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

    def get(self, request, pk, sub_pk, *args, **kwargs):
        template = 'marks/addmark.html'
        students_unit = get_object_or_404(StudentsUnit, pk=pk)
        subject = get_object_or_404(Subject, pk=sub_pk)
        context = {'students_unit': students_unit, 'subject': subject}

        return render(request, template, context)
        
    def post(self, request, pk, sub_pk, *args, **kwargs):
        pass