from django import template

register = template.Library()

MONTHS_KAA = [
    "", "yanvar", "fevral", "mart", "aprel", "may", "iyun",
    "iyul", "avgust", "sentyabr", "oktyabr", "noyabr", "dekabr"
]

@register.filter
def format_kaa_date(value):
    if not value:
        return ''
    try:
        day = value.day
        month = MONTHS_KAA[value.month]
        year = value.year
        return f"{day}-{month} {year}-jıl"
    except AttributeError:
        return ''
