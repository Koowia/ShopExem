from django import template

register = template.Library()

@register.filter
def pluralize_ru(count, variants):
    variants = variants.split(',')
    count = abs(int(count))
    remainder_100 = count % 100
    remainder_10 = count % 10

    if 11 <= remainder_100 <= 19:
        return f"{count} {variants[2]}"
    elif remainder_10 == 1:
        return f"{count} {variants[0]}"
    elif 2 <= remainder_10 <= 4:
        return f"{count} {variants[1]}"
    else:
        return f"{count} {variants[2]}"
