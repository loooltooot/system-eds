from django import template
from django.utils import timezone

from marks.models import Mark

register = template.Library()

@register.inclusion_tag('marks/templatetags/marks_table.html', takes_context=True)
def marks_table(context, students_unit, subject, is_student=False):
    today = timezone.now().date()
    month_ago = today - timezone.timedelta(days=30)
    dates = []

    current_date = month_ago
    while current_date <= today:
        dates.append(current_date)
        current_date += timezone.timedelta(days=1)

    marks = {}

    if is_student:
        student = context['request'].user
        marks[student] = Mark.objects.filter(student=student, subject=subject)
    else:
        for student in students_unit.user_set.all():
            marks[student] = Mark.objects.filter(student=student, subject=subject)

    context['marks_map'] = marks
    context['dates'] = dates

    return context