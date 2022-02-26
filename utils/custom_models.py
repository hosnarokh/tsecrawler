from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from khayyam import JalaliDatetime

from utils.custom_fields import FarsiTextField

'''
set of custom models to use in apps
'''


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super(ActiveManager, self).get_queryset().filter(active=True)


class BaseModel(models.Model):
    """
    a abstract model - it's preferred for all models to inheritance from this model
    """
    description = FarsiTextField(verbose_name=_('Description'), blank=True)
    active = models.BooleanField(verbose_name=_('Active Status'), default=True)
    updated_time = models.DateTimeField(verbose_name=_('Modified On'), auto_now=True)
    created_time = models.DateTimeField(verbose_name=_('Creation On'), auto_now_add=True, db_index=True)

    objects = models.Manager()
    actives = ActiveManager()

    class Meta:
        abstract = True

    @property
    def jalali_updated_time(self):
        if self.updated_time:
            return JalaliDatetime(timezone.localtime(self.updated_time)).strftime('%H:%M %y/%m/%d')
        return None

    @property
    def jalali_created_time(self):
        if self.created_time:
            return JalaliDatetime(timezone.localtime(self.created_time)).strftime('%H:%M %y/%m/%d')
        return None

    jalali_created_time.fget.short_description = _("Creation On")
    jalali_updated_time.fget.short_description = _("Modified On")


class TimeStampModel(models.Model):
    """
    a abstract model - it's preferred for all models to inheritance from this model
    """
    active = models.BooleanField(verbose_name=_('Active Status'), default=True)
    updated_time = models.DateTimeField(verbose_name=_('Modified On'), auto_now=True)
    created_time = models.DateTimeField(verbose_name=_('Creation On'), auto_now_add=True, db_index=True)

    objects = models.Manager()
    actives = ActiveManager()

    class Meta:
        abstract = True

    @property
    def jalali_updated_time(self):
        if self.updated_time:
            return JalaliDatetime(timezone.localtime(self.updated_time)).strftime('%H:%M %y/%m/%d')
        return None

    @property
    def jalali_created_time(self):
        if self.created_time:
            return JalaliDatetime(timezone.localtime(self.created_time)).strftime('%H:%M %y/%m/%d')
        return None

    jalali_created_time.fget.short_description = _("Creation On")
    jalali_updated_time.fget.short_description = _("Modified On")