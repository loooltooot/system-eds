from django import template

from marks.models import Mark

register = template.Library()

def get_average_mark(context, subject, student=None):
    user = context['request'].user

    if student:
        user = student

    marks = Mark.objects.filter(subject=subject, student=user)
    
    if marks.count() == 0:
        return None

    return round(sum([mark.value for mark in marks]) / marks.count() * 100) / 100

@register.simple_tag(takes_context=True)
def average_mark(context, subject, student=None):
     return get_average_mark(context, subject, student)