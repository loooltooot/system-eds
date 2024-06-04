from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseBadRequest, HttpResponseForbidden

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

        context['courses'] = set([appointment.course for appointment in context['related_appointments']])
        context['course'] = request.session.get('course', None)
        context['term'] = request.session.get('term', None)

        if context['course']:
            context['related_appointments'] = context['related_appointments'].filter(course=context['course'])

        if context['term']:
            context['related_appointments'] = context['related_appointments'].filter(is_first_term=context['term'])

        return render(request, template, context)
    
    def post(self, request, *args, **kwargs):
        template = 'marks/dashboard/student.html'
        context = {'related_appointments': Appointment.objects.filter(students_unit=request.user.students_unit)}

        if request.user.groups.filter(name='Преподаватели').exists():
            template = 'marks/dashboard/teacher.html'
            context['related_appointments'] = Appointment.objects.filter(teacher=request.user)

        context['courses'] = set([appointment.course for appointment in context['related_appointments']])
        context['course'] = request.POST.get('course', None) 
        context['term'] = request.POST.get('term', None) if context['course'] is not None else None
        request.session['course'] = context['course']
        request.session['term'] = context['term']

        if context['course']:
            context['related_appointments'] = context['related_appointments'].filter(course=context['course'])

        if context['term']:
            context['related_appointments'] = context['related_appointments'].filter(is_first_term=context['term'])

        return render(request, template, context)
    
class AddMarkView(LoginRequiredMixin, PermissionRequiredMixin, AdminRedirectMixin, View):
    permission_required = 'marks.add_mark'

    def post(self, request, pk, *args, **kwargs):
        appointment = get_object_or_404(Appointment, pk=pk)

        if appointment.teacher != request.user:
            return HttpResponseForbidden()

        form = MarkForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('marks:show', pk=pk)
        
        return HttpResponseBadRequest()
    
class EditMarkView(LoginRequiredMixin, PermissionRequiredMixin, AdminRedirectMixin, View):
    permission_required = 'marks.add_mark'
    
    def post(self, request, pk, *args, **kwargs):
        appointment = get_object_or_404(Appointment, pk=pk)
        mark = get_object_or_404(Mark, pk=request.POST['id'])
        new_feedback = request.POST.get('feedback', mark.feedback).strip()
        new_value = request.POST.get('value', mark.value)
        is_final = request.POST.get('is_final', False)

        if appointment.teacher != request.user:
            return HttpResponseForbidden()

        if new_value not in ['2', '3', '4', '5', '+', '.', '/', 'H']:
            return HttpResponseBadRequest()
        
        if mark.value not in ['+', '.', '/'] and mark.value != new_value:
            return HttpResponseBadRequest()
        
        if is_final: 
            if new_value not in ['2', '3', '4', '5']:
                return HttpResponseBadRequest()
            
            mark.is_final = True

        if new_feedback != mark.feedback:
            mark.feedback = new_feedback

        if new_value != mark.value:
            mark.value = new_value

        mark.save()
        return redirect('marks:show', pk=pk)

class ShowMarksView(LoginRequiredMixin, AdminRedirectMixin, View):
    template = 'marks/addmark.html'

    def get(self, request, pk, *args, **kwargs):
        appointment = get_object_or_404(Appointment, pk=pk)
        context = {'appointment': appointment}

        if request.user.groups.filter(name='Студенты').exists():
            if appointment.students_unit != request.user.students_unit:
                return HttpResponseForbidden()
            context['is_student'] = True

        if request.user.groups.filter(name='Преподаватели').exists():
            if appointment.teacher != request.user:
                return HttpResponseForbidden()

        return render(request, self.template, context)