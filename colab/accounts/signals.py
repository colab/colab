
from django.dispatch import receiver, Signal
from django.db.models.signals import post_save

user_created = Signal(providing_args=['user', 'password'])
user_password_changed = Signal(providing_args=['user', 'password'])
