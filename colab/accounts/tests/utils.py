from django.forms import ValidationError


def password_validator(password):
    raise ValidationError('Test error')


def username_validator(username):
    raise ValidationError('Test error')
