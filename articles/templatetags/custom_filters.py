from django import template

register = template.Library()

MONTHS_KAA = [
    "", "Yanvar", "Fevral", "Mart", "Aprel", "May", "Iyun",
    "Iyul", "Avgust", "Sentyabr", "Oktyabr", "Noyabr", "Dekabr"
]

@register.filter
def format_kaa_date(value):
    if not value:
        return ''
    try:
        day = value.day
        month = MONTHS_KAA[value.month]
        year = value.year
        return f"{day} {month} {year}"
    except AttributeError:
        return ''
