# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-18 18:31
from __future__ import unicode_literals

import app.user_management.models
from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0007_alter_validators_add_error_messages'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('timezone', models.CharField(default='America/New_York', max_length=50)),
                ('gender', models.CharField(blank=True, choices=[('m', 'Male'), ('f', 'Female'), ('u', 'Undefined')], max_length=1, null=True)),
                ('birthdate', models.DateField(blank=True, null=True)),
                ('locale', models.CharField(blank=True, default='en-us', max_length=10, null=True)),
                ('hash_code', models.CharField(blank=True, db_index=True, default=app.user_management.models._createHash, max_length=32, null=True)),
                ('deleted', models.BooleanField(db_index=True, default=False)),
                ('activated', models.BooleanField(db_index=True, default=False)),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'db_table': 'auth_user_extended',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
