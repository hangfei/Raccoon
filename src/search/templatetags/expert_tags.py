from django import template
from datetime import date, timedelta

register = template.Library()

@register.filter(name='half_round_rating')
def half_round_rating(value):
    half_round_rating = round(float(value) * 2) / 2
    return half_round_rating