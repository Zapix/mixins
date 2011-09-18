from django.db import models
from django.utils.translation import ugettext_lazy as _

class CreatedUpdatedMixin(object):
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True)
