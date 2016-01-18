# -*- coding: utf-8 -*-
from django.db import models
from tastypie.models import create_api_key
from django.contrib.auth.models import User, UserManager
from django.utils.translation import ugettext_lazy as _

import uuid

def _createHash():
    uid = uuid.uuid4()
    return uid.hex


class CustomUser(User):

    GENDER_CHOICES = (
        ('m', _('Male')),
        ('f', _('Female')),
        ('u', _('Undefined')),
    )

    timezone = models.CharField(max_length=50, default='America/New_York')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    birthdate = models.DateField(null=True, blank=True)
    locale = models.CharField(max_length=10, blank=True, null=True, default='en-us')
    hash_code = models.CharField(max_length=32, default=_createHash, null=True, blank=True, db_index=True)
    deleted = models.BooleanField(default=False, db_index=True)
    activated = models.BooleanField(default=False, db_index=True)

    # Use UserManager to get the create_user method, etc.
    objects = UserManager()

    class Meta:
        db_table = 'auth_user_extended'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

models.signals.post_save.connect(create_api_key, sender=User)