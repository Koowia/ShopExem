from django import template
from decimal import Decimal, InvalidOperation


register = template.Library()


@register.simple_tag(takes_context=True)
def get_cart_count(context):
    request = context['request']
    if hasattr(request, 'cart'):
        return request.cart.total_items
    return 0


@register.filter
def multiply(value, arg):
    try:
        return Decimal(str(value)) * Decimal(str(arg))
    except (InvalidOperation, TypeError):
        return Decimal('0')