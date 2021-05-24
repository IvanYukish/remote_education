from django.template.defaulttags import register


@register.simple_tag(takes_context=True)
def get_by_pk(context, pk):
    pk = f'form_{pk}'
    return context[pk]
