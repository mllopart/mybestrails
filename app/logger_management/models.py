# -*- coding: utf-8 -*-
from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from apps.core.models import TimeStampedModel

# Create your models here.
class mdlLog(TimeStampedModel):
    
    action_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name="UsuariLog", db_index=True)
    content_type = models.ForeignKey(ContentType, related_name="ContentTypeLog", db_index=True)
    object_id = models.IntegerField()
    action = models.CharField(max_length=25)
    comments = models.CharField(max_length=255, null=True, blank=True)    
    
    def __unicode__(self):
        return self.action
    
    class Meta:
        db_table = 'action_log'
        verbose_name = 'Log'
        verbose_name_plural = 'Logs'