from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def version_label(context):
    user = context['request'].user
    if user.groups.filter(name='Преподаватели').exists():
        return 'версия для преподавателей'
    
    return 'версия для студентов'