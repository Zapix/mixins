# -*- coding: utf-8 -*-
from django.db.models import Manager
from django.db.models.query import QuerySet


class EnableQuerySet(QuerySet):
    '''
    Mixin for query set
    '''
    def enable(self):
        return self.filter(enable=True)


class EnableManager(Manager):
    '''
    Extends Manager
    '''
    def get_query_set(self):
        return EnableQuerySet(self.model, using=self._db)

    def enable(self):
        return self.get_query_set().enable()
