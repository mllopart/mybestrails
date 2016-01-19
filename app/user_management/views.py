# -*- coding: utf-8 -*-
from app.user_management.forms import login_form
from app.logger_management.models import mdlLog
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib import auth 
import logging
from datetime import timedelta
from django.views.decorators.cache import never_cache
from django.utils.translation import ugettext_lazy as _


# Create your views here.
@never_cache
def vw_logout_page(request):
    
    #we keep track of the user movements at the log
    try:
        lo = mdlLog()
        lo.user = request.user
        lo.content_type = ContentType.objects.get(model = 'user')
        lo.object_id = request.user.id
        lo.action = 'logout'
        lo.save()
        
    except Exception as e:
        logging.error(e)
    
    auth.logout(request)
        
    #redirect to home
    return HttpResponseRedirect(reverse('homepage'))

@never_cache
def vw_login_page(request):    

    mesage = None
    error = None

    
    #redirect_to = request.REQUEST.get('next', '')
    redirect_to = ""
    
    if not redirect_to:
        redirect_to = 'homepage'    

    if request.user.is_authenticated():       
        
        print("is_authenticated")
        print(request.user)
        return HttpResponseRedirect(reverse('homepage'))
    
    else:
        if request.method == 'POST':
            
            print("NOT is_authenticated - POST")
            form = login_form(request.POST)
            form.helper.form_action = reverse('login') + '?next=' + redirect_to
            
            if form.is_valid():
                f = form.cleaned_data
                
                try:
                    user = auth.authenticate(username=f['user'], password=f['password'])
                except:
                    user = None
                    pass
                
                if user is not None and user.is_active:
                    
                    #log
                    try:
                        lo = mdlLog()
                        lo.user = request.user
                        lo.content_type = ContentType.objects.get(model = 'user')
                        lo.object_id = request.user.id
                        lo.action = 'login'
                        lo.save()
                        
                    except Exception as e:
                        logging.error(e)
                    
                    request.session.set_expiry(timedelta(days=settings.KEEP_LOGGED_DURATION))
                    
                    try:
                        from tastypie.models import ApiKey 
                        
                        #we create an api key
                        api = ApiKey()
                        api.user = user
                        api.save()
                    except Exception as e:
                        logging.error(e)
                        
                    if request.session.test_cookie_worked():            
                        request.session.delete_test_cookie()

                    auth.login(request, user) 
                    
                    request.session['welcome_msg'] = _('Welcome ') + user.username + '.'               
                    
                    return HttpResponseRedirect(reverse('homepage'))                    
                    
                else:                                
                    error = _('User or password not in our systems')                           
                    return render_to_response('login/login.html', {
                                                              'form': form,
                                                              'mesage': mesage,
                                                              'error': error,
                                                              'redirect_to': redirect_to,
                                                              }, context_instance=RequestContext(request))
            else:                
                error = _('User or password not in our systems')                
                return render_to_response('login/login.html', {
                                                          'form': form,
                                                          'mesage': mesage,
                                                          'error': error,
                                                          'redirect_to': redirect_to,
                                                          }, context_instance=RequestContext(request))
        else:
            
            print("NOT is_authenticated - NOT POST")
            form = login_form()            
            return render_to_response('login/login.html', {
                                                              'form': form,
                                                              'mesage': mesage,
                                                              'error': error,
                                                              'redirect_to': redirect_to,
                                                              }, context_instance=RequestContext(request))

