from functools import wraps
from django.db import models
from django.utils.translation import ugettext_lazy as _

from mixins.managers import EnableManager
from mixins.exceptions import DecoratorMixinException

class CreatedUpdatedMixin(models.Model):
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True)

    class Meta:
        abstract=True

def Enable(cls=None, status=True, set_manager=True, mixin=False):
    '''
    Adds enable field into cls or return mixin
    :param cls: class that would updates
    :param status: default value for enable field
    :type status: bool
    :param set_manager: sets is EnableManager is required
    :type set_manager: bool
    :param mixin: sets should be returns model mixin
    :type mixin: bool
    '''
    if cls is None and mixin:
        class Class(models.Model):
            enbale = models.BooleanField(_('Enable'), default=status)
            class Meta:
                abstract = True
        if set_manager == True:
            Class.add_to_class('objects', EnableManager())
            Class.add_to_class('_base_manager', EnableManager())
        return Class
    elif cls is None and not mixin:
        def decorator(cls):
            cls.add_to_class('enable',
                             models.BooleanField(_('Enable'), default=status))
            if set_manager == True:
                cls.objects = EnableManager()
            return cls
        return decorator
    elif not cls is None and not mixin:
        cls.add_to_class('enable',
                         models.BooleanField(_('Enable'), default=status))
        if set_manager == True:
            cls.objects = EnableManager()
        return cls
    elif not cls is None and not mixin:
        raise DecoratorMixinException

EnableTrueMixin = Enable(mixin=True)
EnableFalseMixin = Enable(status=False, mixin=True)
