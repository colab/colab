
from django.dispatch import Signal


user_password_changed = Signal(providing_args=['user', 'password'])
