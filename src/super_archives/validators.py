# -*- coding: utf-8 -*-

from django.core.exceptions import ValidationError

class UniqueValidator(object):
    
    def __init__(self, model, field_name):
        self.model = model
        self.field_name = field_name
        
    def __call__(self, value):
        result = self.model.objects.filter(**{self.field_name: value})
        if result:
            msg = u'Já existente. Escolha outro.'
            raise ValidationError(msg)
