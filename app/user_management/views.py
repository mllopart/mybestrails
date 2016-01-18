# -*- coding: utf-8 -*-
from django.shortcuts import render
from models import CustomUser
from forms import login_form
from app.logger_management.models import mdlLog
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

# Create your views here.

def vw_logout_page(request):
    
    #guardem el log
    try:
        lo = mdlLog()
        lo.user = request.user
        lo.content_type = ContentType.objects.get(model = 'user')
        lo.object_id = request.user.id
        lo.action = 'logout'
        lo.save()
        
    except Exception, e:
        logging.error(e)
    
    auth.logout(request)
        
    #redirect to home
    return HttpResponseRedirect(reverse('home'))


def vw_login_page(request):    

	mesage = None
    error = None
    
    redirect_to = request.REQUEST.get('next', '')
    
    if not redirect_to:
        redirect_to = 'home'    

    if request.user.is_authenticated():       
        
        return HttpResponseRedirect(reverse('home'))
    
    else:
        if request.method == 'POST':
            
            form = login_form(request.POST)
            form.helper.form_action = reverse('vw_login_page') + '?next=' + redirect_to
            
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
                        
                    except Exception, e:
                        logging.error(e)
                    
                    request.session.set_expiry(timedelta(days=settings.KEEP_LOGGED_DURATION))
                    
                    try:
                        from tastypie.models import ApiKey 
                        
                        #we create an api key
                        api = ApiKey()
                        api.user = user
                        api.save()
                    except Exception, e:
                        print e
                        logging.error(e)
                        
                    if request.session.test_cookie_worked():            
                        request.session.delete_test_cookie()

                    auth.login(request, user) 
                    
                    request.session['welcome_msg'] = 'Welcome ' + user.username + '.'               
                    
                    return HttpResponseRedirect(reverse('home'))                    
                    
                else:                                
                    error = u'L\'usuari o la contrassenya és incorrecta'.encode('utf-8').decode('utf-8')         
                    return render_to_response('principal/usuari/login.html', {
                                                              'form': form,
                                                              'mesage': mesage,
                                                              'error': error,
                                                              'redirect_to': redirect_to,
                                                              }, context_instance=RequestContext(request))
            else:                
                error = u'L\'usuari o la contrassenya és incorrecta'.encode('utf-8').decode('utf-8')       
                return render_to_response('principal/usuari/login.html', {
                                                          'form': form,
                                                          'mesage': mesage,
                                                          'error': error,
                                                          'redirect_to': redirect_to,
                                                          }, context_instance=RequestContext(request))
        else:
            form = login_form()
            form.helper.form_action = reverse('login_view_super') + '?next=' + redirect_to
            return render_to_response('principal/usuari/login.html', {
                                                              'form': form,
                                                              'mesage': mesage,
                                                              'error': error,
                                                              'redirect_to': redirect_to,
                                                              }, context_instance=RequestContext(request))

vw_login_page = never_cache (vw_login_page) 
vw_logout_page = never_cache (vw_logout_page)