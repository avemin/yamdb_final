import datetime as dt

from django.core.exceptions import ValidationError


def validate_year(value):
    if value < 1895 or value > dt.datetime.now().year:
        raise ValidationError('Неверный год.')
