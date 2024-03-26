from django import template

from marks.models import Mark

register = template.Library()

@register.inclusion_tag('marks/templatetags/marks_table.html')
def marks_table(student, subject):
    marks = Mark.objects.filter(student=student, subject=subject)
    dates = [mark.pub_date for mark in marks]
    return {'marks': marks, 'dates': dates}