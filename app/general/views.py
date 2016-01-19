# -*- coding: utf-8 -*-
from django.template import RequestContext
from django.shortcuts import render_to_response

# Create your views here.
def vw_homepage(request):
      
    return render_to_response('homepage/homepage.html', {'request':request},
                          context_instance=RequestContext(request))
