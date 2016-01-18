# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^logout/$', views.vw_logout_page, name='logout'),
    url(r'^login/$', views.vw_login_page, name='login'),
]