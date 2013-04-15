from django.db import models
from django.utils.translation import ugettext_lazy as _

from mixins import managers
from mixins.exceptions import DecoratorMixinException

class CreatedUpdatedMixin(models.Model):
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True)

    class Meta:
        abstract=True

def enable_mixin(cls=None, status=True, set_manager=True, mixin=False):
    '''
    Adds enable field into cls or return mixin
    :param cls: class that would updates
    :param status: default value for enable field
    :type status: bool
    :param set_manager: sets if EnableManager is required
    :type set_manager: bool
    :param mixin: sets should be returned model mixin
    :type mixin: bool
    '''
    def decorator(cls):
        '''
        Adds field and manager if manager is required
        '''
        cls.add_to_class('enabled',
                         models.BooleanField(_('Enabled'), default=status))
        if set_manager:
            cls.add_to_class('objects', managers.EnableManager())
        return cls

    class Class(models.Model):
        '''
        Enable AbstractModels
        '''
        enabled = models.BooleanField(_('Enabled'), default=status)

        class Meta:
            abstract = True

    if cls and mixin:
        raise DecoratorMixinException
    elif mixin:
        if set_manager:
            Class.add_to_class('objects', managers.EnableManager())
        return Class
    elif cls:
        return decorator(cls)
    else:
        return decorator

EnableTrueMixin = enable_mixin(mixin=True)
EnableFalseMixin = enable_mixin(status=False, mixin=True)

def start_expire_mixin(cls=None, expire_date_required=False,
                       set_manager=True, mixin=False):
    '''
    Adds start_date, expire_Date fields into cls or return mixin
    :param cls: class that would updates
    :param expire_date_required: 
    :type expire_date_required: bool
    :param set_manager: sets if EnableManager is required
    :type set_manager: bool
    :param mixin: sets should be returned model mixin
    :type mixin: bool
    '''
    def decorator(cls):
        '''
        Adds fields and manager if manager is required
        '''
        cls.add_to_class('start_date', models.DateTimeField(_('Start date')))
        if expire_date_required:
            cls.add_to_class('expire_date',
                             models.DateTimeField(_('Expire date')))
        else:
            cls.add_to_class('expire_date',
                             models.DateTimeField(_('Expire date'),
                                                  blank=True, null=True))
        if set_manager:
            cls.add_to_class('objects',
                             managers.StartExpireManager())
        return cls
    
    class Class(models.Model):
        class Meta:
            abstract = True
    
    if cls and mixin:
        raise DecoratorMixinException
    elif mixin:
        return decorator(Class)
    elif cls:
        return decorator(cls)
    else:
        return decorator
