# -*- coding: utf-8 -*-
from django.db import models
from autoslug.fields import AutoSlugField
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
import uuid

def _createHash():
    uid = uuid.uuid4()
    return uid.hex

class mdlTrack(models.Model):
    name = models.CharField(max_length=4000, help_text=_('GPS name of track.'))
    cmt = models.TextField (null=True, blank=True, help_text=_('GPS comment for track.'))
    desc = models.TextField(null=True, blank=True, help_text=_('ser description of track.'))
    src = models.CharField(max_length=100,null=True, blank=True, help_text=_('Source of data. Included to give user some idea of reliability and accuracy of data.'))
    link = models.URLField(null=True, blank=True, help_text=_('Links to external information about track.'))
    number =  models.IntegerField(default=1, help_text=_('GPS track number.'))
    type= models.CharField(max_length=100,null=True, blank=True, help_text=_('Type (classification) of track.'))
    creation_user = models.ForeignKey(User, related_name="usuari_soci", db_index=True)
    #slug = AutoSlugField(populate_from='name', always_update=False, unique_with='name', null=True, blank=True, db_index=True)
    hash_code = models.CharField(max_length=32,default=_createHash,null=True, blank=True,db_index=True)
    deleted = models.BooleanField(default=False, help_text=_('Is the track deleted?'))
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'track'
        verbose_name = 'Track'
        verbose_name_plural = 'Tracks'
        ordering = ('name',)

