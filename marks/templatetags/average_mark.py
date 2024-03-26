from django import template

from marks.models import Mark

register = template.Library()

@register.simple_tag(takes_context=True)
def average_mark(context, subject, student=None):
    user = context['request'].user
    marks = Mark.objects.filter(subject=subject, student=user)

    if student:
        marks = Mark.objects.filter(subject=subject, student=student)

    if marks.count() == 0:
        return 'оценок еще нет'

    return round(sum([mark.value for mark in marks]) / marks.count() * 100) / 100