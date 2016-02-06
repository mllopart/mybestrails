# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

app_name = 'general'

urlpatterns = [
    url(r'^$', views.vw_homepage, name='homepage'),
]