# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

app_name = 'track_management'


urlpatterns = [
    url(r'^uploadGPX/$', views.upload_gpx, name='gpxUpload'),
    url(r'^userListTracks/$', views.vw_list_user_tracks, name='userListTracks'),
    url(r'^userListTracks/(?P<track_hash>[^/]+)/$', views.vw_view_user_track_detail, name='userTrackDetails'),
]