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

@register.simple_tag(takes_context=True)
def average_mark(context, subject, student=None):
    if student is None:
        student = context['request'].user

    return get_average_mark(subject, student)