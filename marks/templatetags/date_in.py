from django import template

register = template.Library()

@register.simple_tag
def date_in(marks, date):
    for mark in marks:
        if date == mark.pub_date:
            return True
        
    return False