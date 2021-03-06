# -*- coding: utf-8 -*-
from django import forms
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _

class UploadGpxForm(forms.Form):

    gpxfile = forms.FileField(
        label=_('Select a file'),
        required = True,
    )
    
    title = forms.CharField(
        label=_('Track title'),
        required = True,
    )
    
    description = forms.CharField(
        label=_('Track description'),
        required = True,
    )
    
    

    def clean_gpxfile(self):
        uploaded_file = self.cleaned_data['gpxfile']
        print ('Uploaded file type: ' + uploaded_file.content_type)

        content_type = uploaded_file.content_type
        
        allowed_content_types = ['text/xml', 'application/octet-stream']
        
        if content_type in allowed_content_types:
            
            if uploaded_file._size > 22621440:
                raise forms.ValidationError(_('Please keep filesize under 21 MB. Current filesize %s') % (filesizeformat(uploaded_file._size)))
         
        else:
            raise forms.ValidationError(_('Filetype not supported.'))

        return uploaded_file