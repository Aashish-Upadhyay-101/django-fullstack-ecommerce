from django import template

register = template.Library()

@register.filter
def item_total(quantity, price):
    return quantity * float(price)


@register.filter
def grand_total(items):
    total = sum([(item.quantity * item.product.price) for item in items])
    return total

