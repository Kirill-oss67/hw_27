from datetime import date

from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError

MIN_USER_AGE = 9
FORBIDDEN_DOMENS = ["rambler.ru"]


def check_birthday(value):
    diff = relativedelta(date.today(), value).years
    if diff < MIN_USER_AGE:
        raise ValidationError("the user with this age is too young")


def check_email(value):
    mail_domen = value.split('@')[-1]
    if mail_domen in FORBIDDEN_DOMENS:
        raise ValidationError("this domen is forbidden")
