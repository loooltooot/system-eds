from django import template
from .average_mark import get_average_mark
from decimal import getcontext, ROUND_HALF_DOWN, Decimal

register = template.Library()

@register.inclusion_tag('marks/templatetags/average_mark_inclusion.html', takes_context=True)
def average_mark_inclusion(context, appointment):
    decimal_context = getcontext()
    decimal_context.rounding = ROUND_HALF_DOWN

    IMGS = {
        5: 'marks/imgs/3dmarks/5red.png',
        4: 'marks/imgs/3dmarks/4red.png',
        3: 'marks/imgs/3dmarks/3red.png',
        2: 'marks/imgs/3dmarks/2red.png',
    }

    module_context = {}

    module_context['average_mark'], module_context['is_final'] = get_average_mark(appointment, student=context['request'].user, return_status=True)
    if module_context['average_mark'] is not None:
        module_context['img_src'] = IMGS[round(Decimal(module_context['average_mark']), 0)]

    return module_context