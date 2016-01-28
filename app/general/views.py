# -*- coding: utf-8 -*-
from django.template import RequestContext
from django.shortcuts import render

# Create your views here.
def vw_homepage(request):
      
    return render(request,'homepage/homepage.html', {'request':request}
                          )
