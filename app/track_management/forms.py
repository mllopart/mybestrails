# -*- coding: utf-8 -*-
from django import forms
from app.track_management.models import mdlGPXFile
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _

class UploadGpxForm(forms.Form):

    gpxfile = forms.FileField(
        label='Select a file',
    )

    def clean_gpx_file(self):
        uploaded_file = self.cleaned_data['gpxfile']
        print (uploaded_file.content_type)

        #content_type = uploaded_file.content_type
        #allowed_content_types = ['text/xml', 'application/octet-stream']
        #if content_type in allowed_content_types:
        #    if uploaded_file._size > 2621440:
        #        raise forms.ValidationError(_('Please keep filesize under 2.5 MB. Current filesize %s') % (filesizeformat(uploaded_file._size)))
        # 
        #else:
        #    raise forms.ValidationError(_('Filetype not supported.'))

        return uploaded_file 