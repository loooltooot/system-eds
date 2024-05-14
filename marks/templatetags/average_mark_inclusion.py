from django import template
from .average_mark import get_average_mark

register = template.Library()

@register.inclusion_tag('marks/templatetags/average_mark_inclusion.html', takes_context=True)
def average_mark_inclusion(context, subject):
    IMGS = {
        5: 'marks/imgs/3dmarks/5red.png',
        4: 'marks/imgs/3dmarks/4red.png',
        3: 'marks/imgs/3dmarks/3red.png',
        2: 'marks/imgs/3dmarks/2red.png',
    }

    context['average_mark'] = get_average_mark(context, subject)
    context['img_src'] = IMGS[5]
    # if context['average_mark'] != None:
    #     context['img_src'] = IMGS[round(context['average_mark'])]

    return context