# -*- coding: utf-8 -*-
from django import template
from django.conf import settings

register = template.Library()

# Custom tag for diagnostics
@register.simple_tag()
def debug_object_dump(var):
    output = None
    
    try:
        output = vars(var)
    except Exception as e:
        if settings.DEBUG: print(e)
        output = 'err'
    
    
    return output

#custom tag to show google analytics
@register.simple_tag()
def googleanalyticsjs(user):
    code =  getattr(settings, "GOOGLE_ANALYTICS_CODE", False)
    
    if not code:
        return "<!-- Goggle Analytics not included because you haven't set the settings.GOOGLE_ANALYTICS_CODE variable! -->"

    if user.is_staff:
        return "<!-- Goggle Analytics not included because you are a staff user! -->"

    if settings.DEBUG:
        return "<!-- Goggle Analytics not included because you are in Debug mode! -->"

    
    return  """
    <script>
      (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
      (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
      m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
      })(window,document,'script','//www.google-analytics.com/analytics.js','ga');
    
      ga('create', '""" + str(code) + """', 'auto');
      ga('send', 'pageview');
    
    </script>
    """