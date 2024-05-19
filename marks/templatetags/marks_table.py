from django import template
from django.utils import timezone

from marks.models import Mark

register = template.Library()

@register.inclusion_tag('marks/templatetags/marks_table.html', takes_context=True)
def marks_table(context, students_unit, subject, is_student=False):
    marks = {}

    if is_student:
        student = context['request'].user
        marks[student] = Mark.objects.filter(student=student, subject=subject)
    else:
        for student in students_unit.user_set.all().order_by('surname'):
            marks[student] = student.received_marks.filter(subject=subject)
    
    dates = set()
    for key in marks.keys():
        for mark in marks[key]:
            dates.add(mark.pub_date)

    context['marks_map'] = marks
    context['dates'] = sorted(dates)

    return context