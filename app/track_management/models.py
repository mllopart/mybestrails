# -*- coding: utf-8 -*-
from django.contrib.gis.db import models
#from autoslug.fields import AutoSlugField
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.contrib.gis import admin as geoadmin
import uuid

def _createHash():
    uid = uuid.uuid4()
    return uid.hex

def GPX_Folder(instance, filename):
    return "uploaded_gpx_files/%s" % (filename)

class mdlTrack(models.Model):
    
    TRACK_TYPES = (
        ('gpx', _('GPX')),
        ('klm', _('KLM')), 
        ('fir', _('FIT')),
    )
    
    name = models.CharField(max_length=4000, help_text=_('GPS name of track.'))
    description = models.TextField(null=True, blank=True, help_text=_('User description of track.'))
    type= models.CharField(max_length=3, choices=TRACK_TYPES, blank=True, null=True, help_text=_('Track type.'))
    creation_user = models.ForeignKey(User, db_index=True)
    hash_code = models.CharField(max_length=32,default=_createHash,null=True, blank=True,db_index=True)
    deleted = models.BooleanField(default=False, help_text=_('Is the track deleted?'))
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)
    
    #cmt = models.TextField (null=True, blank=True, help_text=_('GPS comment for track.'))    
    #src = models.CharField(max_length=100,null=True, blank=True, help_text=_('Source of data. Included to give user some idea of reliability and accuracy of data.'))
    #link = models.URLField(null=True, blank=True, help_text=_('Links to external information about track.'))
    #number =  models.IntegerField(default=1, help_text=_('GPS track number.'))       
    #slug = AutoSlugField(populate_from='name', always_update=False, unique_with='name', null=True, blank=True, db_index=True)       

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'track'
        verbose_name = 'Track'
        verbose_name_plural = 'Tracks'
        ordering = ('name',)
        
class mdlGPXFile(models.Model):
    title = models.CharField("Title", max_length=4000)
    gpx_file = models.FileField(upload_to=GPX_Folder, blank=True)
    track = models.ForeignKey(mdlTrack, db_index=True)

    def __unicode__(self):
        return self.title

    class Meta:
        db_table = 'GPX_File'
        verbose_name = 'GPX_File'
        verbose_name_plural = 'GPX_Files'
    
    
class mdlGPXPoint(models.Model):
    name = models.CharField("Name", max_length=50, blank=True)
    description = models.CharField("Description", max_length=250, blank=True)
    gpx_file = models.ForeignKey(mdlGPXFile)
    point = models.PointField()
    objects = models.GeoManager()

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        db_table = 'GPX_Point'
        verbose_name = 'GPX_Point'
        verbose_name_plural = 'GPX_Points'

class mdlGPXTrack(models.Model):
    track = models.MultiLineStringField()
    gpx_file = models.ForeignKey(mdlGPXFile)
    objects = models.GeoManager()

    class Meta:
        db_table = 'GPX_Track'
        verbose_name = 'GPX_Track'
        verbose_name_plural = 'GPX_Tracks'

geoadmin.site.register(mdlGPXPoint, geoadmin.OSMGeoAdmin)
geoadmin.site.register(mdlGPXTrack, geoadmin.OSMGeoAdmin)
admin.site.register(mdlGPXFile)

