from django import template

from marks.models import Mark

register = template.Library()

def get_average_mark(subject, student):
    marks = Mark.objects.filter(subject=subject, student=student)
    
    if marks.count() == 0:
        return None

    int_marks = []
    for mark in marks:
        try:
            parsed_mark = int(mark.value)
            int_marks.append(parsed_mark)
        except ValueError:
            pass

    if len(int_marks) == 0:
        return None

    return round(sum(int_marks) / len(int_marks) * 100) / 100

@register.inclusion_tag('marks/templatetags/average_mark.html', takes_context=True)
def average_mark(context, subject, student=None):
    if student is None:
        student = context['request'].user

    average_mark = get_average_mark(subject, student)
    module_context = {}

    if average_mark is not None:
        module_context['average_mark'] = average_mark
        module_context['floor_mark'] = int(average_mark)
    else: 
        module_context['average_mark'] = '-'

    return module_context