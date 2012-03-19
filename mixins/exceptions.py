# -*- coding: utf-8 -*-
class DecoratorMixinException(Exception):

    def __str__(self):
        return 'Decorator coudn\'t be a class mixin'

