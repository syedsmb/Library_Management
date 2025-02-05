from django import template

register = template.Library()

@register.filter
def sum_total(cart_items):
    total = 0
    for item in cart_items:
        total += item.book.price * item.quantity
    return total

    if not cart_items:
        return 0
    return sum(item.quantity * item.price for item in cart_items)