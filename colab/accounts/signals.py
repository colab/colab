
from django.dispatch import Signal


user_created = Signal(providing_args=['user', 'password'])
user_password_changed = Signal(providing_args=['user', 'password'])
