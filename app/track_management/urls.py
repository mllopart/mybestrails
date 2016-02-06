# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

app_name = 'track_management'


urlpatterns = [
    url(r'^uploadGPX/$', views.upload_gpx, name='gpxUpload'),
]