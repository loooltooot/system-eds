from django import template

from marks.models import Mark

register = template.Library()

@register.simple_tag
def has_final_mark(appointment, student):
    if student.received_marks.filter(appointment=appointment, is_final=True).exists():
        return {'mark': student.received_marks.filter(appointment=appointment, is_final=True).first().value, 'status': True}
    
    return False