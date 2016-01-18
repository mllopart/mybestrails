# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

class login_form(forms.Form):
    
    user = forms.CharField(
                             widget=forms.TextInput(
                                   attrs={'size':'30','class':'required'}
                                   ),
                             label = _('User'),
                             max_length = 30,
                             required = True,
                             help_text = _('Please enter your user'),
                             )
    
    password = forms.CharField(
                                   widget=forms.PasswordInput(
                                                              attrs={'size':'30','class':'required'}
                                                              ),
                                   label = _('Password'),
                                   max_length = 100,
                                   required = True,
                                   help_text = _('Please enter your password'),
                                   )
