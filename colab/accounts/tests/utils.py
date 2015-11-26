
from django.forms import ValidationError

def password_validator(password):
    raise ValidationError('Test error')

