from django import template

from marks.models import Mark

register = template.Library()

@register.inclusion_tag('marks/templatetags/marks_table.html', takes_context=True)
def marks_table(context, students_unit, subject):
    marks = Mark.objects.filter(student__students_unit=students_unit, subject=subject)
    dates = sorted(set([mark.pub_date for mark in marks]))
    marks = {}

    for student in students_unit.user_set.all():
        marks[student] = Mark.objects.filter(student=student, subject=subject)

    context['marks_map'] = marks
    context['dates'] = dates

    return context