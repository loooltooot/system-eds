from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseBadRequest, HttpResponseForbidden
from datetime import datetime

from .models import Appointment, StudentsUnit, Subject, Mark
from .mixins import AdminRedirectMixin
from .forms import MarkForm

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

    def post(self, request, pk, sub_pk, *args, **kwargs):
        students_unit = get_object_or_404(StudentsUnit, pk=pk)
        subject = get_object_or_404(Subject, pk=sub_pk)

        if not Appointment.objects.filter(teacher=request.user, subject=subject, students_unit=students_unit).exists():
            return HttpResponseForbidden()

        form = MarkForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('marks:show', pk=pk, sub_pk=sub_pk)
        
        return HttpResponseBadRequest()
    
class EditMarkView(LoginRequiredMixin, PermissionRequiredMixin, AdminRedirectMixin, View):
    permission_required = 'marks.add_mark'
    
    def post(self, request, pk, sub_pk, *args, **kwargs):
        students_unit = get_object_or_404(StudentsUnit, pk=pk)
        subject = get_object_or_404(Subject, pk=sub_pk)
        mark = get_object_or_404(Mark, pk=request.POST['id'])
        new_feedback = request.POST['feedback']
        new_value = request.POST['value']

        if not Appointment.objects.filter(teacher=request.user, subject=subject, students_unit=students_unit).exists():
            return HttpResponseForbidden()

        if new_value not in ['2', '3', '4', '5', '+', '.', '/', 'H']:
            return HttpResponseBadRequest()
        
        if mark.value not in ['+', '.', '/'] and mark.value != new_value:
            return HttpResponseForbidden()
        
        if new_feedback != mark.feedback:
            mark.feedback = new_feedback

        if new_value != mark.value:
            mark.value = new_value

        mark.save()
        return redirect('marks:show', pk=pk, sub_pk=sub_pk)

class ShowMarksView(LoginRequiredMixin, AdminRedirectMixin, View):
    template = 'marks/addmark.html'

    def get(self, request, pk, sub_pk, *args, **kwargs):
        students_unit = get_object_or_404(StudentsUnit, pk=pk)
        subject = get_object_or_404(Subject, pk=sub_pk)
        context = {'students_unit': students_unit, 'subject': subject}

        if request.user.groups.filter(name='Студенты').exists():
            if not Appointment.objects.filter(students_unit=request.user.students_unit, subject=subject).exists():
                return HttpResponseForbidden()
            context['is_student'] = True

        if request.user.groups.filter(name='Преподаватели').exists():
            if not Appointment.objects.filter(teacher=request.user, subject=subject, students_unit=students_unit).exists():
                return HttpResponseForbidden()

        return render(request, self.template, context)