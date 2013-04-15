# -*- coding: utf-8 -*-
import datetime

from django.db.models import Manager, Q
from django.db.models.query import QuerySet


class EnableQuerySet(QuerySet):
    '''
    Adds enable function for queryset
    '''
    def get_enabled(self):
        return self.filter(enabled=True)


class EnableManager(Manager):
    '''
    Adds EnableQuerySet,
    Adds enable method,
    '''
    def get_query_set(self):
        return EnableQuerySet(self.model, using=self._db)

    def get_enabled(self):
        return self.get_query_set().get_enabled()

class StartExpireQuerySet(QuerySet):
    '''
    Add get_active function for queryset
    '''
    def active(self):
        current_time = datetime.datetime.now()
        time_limit = Q(start_date__lte=current_time,
                        expire_date__gte=current_time)
        from_time = Q(start_date__lte=current_time,
                      expire_date__isnull=True)
        return self.filter(time_limit | from_time)

class StartExpireManager(Manager):
    '''
    Adds EnableQuerySet
    '''
    def get_query_set(self):
        return StartExpireQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_query_set().active()

