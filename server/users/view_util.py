from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.template.context_processors import csrf

# import code for encoding urls and generating md5 hashes
import hashlib
import socket
import logging
from django.conf import settings

from .models import PageView

def fill_template_values(request, **template_args):
    """
        Fill the template argument items needed to populate
        side bars and other satellite items on the pages.
        
        Only the arguments common to all pages will be filled.
    """
    template_args['user'] = request.user
    if request.user.is_authenticated():
        if hasattr(settings, 'GRAVATAR_URL'):
            guess_email = "%s@%s" % (request.user.username, settings.ALLOWED_DOMAIN)
            gravatar_url = settings.GRAVATAR_URL+hashlib.md5(guess_email).hexdigest()+'?d=identicon'
            template_args['gravatar_url'] = gravatar_url
    else:
        request.user.username = 'Guest User'

    template_args['logout_url'] = reverse('reduction_server.users.views.perform_logout')
    redirect_url = reverse('reduction_server.users.views.perform_login')
    redirect_url  += '?next=%s' % request.path
    template_args['login_url'] = redirect_url
    
    # Determine whether the user is using a mobile device
    template_args['is_mobile'] = hasattr(request, 'mobile') and request.mobile
    template_args.update(csrf(request))
    return template_args

def _check_credentials(request):
    """
        Internal utility method to check whether a user has access to a view
    """
    # If we don't allow guests but the user is authenticated, return the function
    if request.user.is_authenticated():
        return True
    
    # If we allow users on a domain, check the user's IP
    elif len(settings.ALLOWED_DOMAIN)>0:
        ip_addr =  request.META['REMOTE_ADDR']
        try:
            # If the user is on the allowed domain, return the function
            if socket.gethostbyaddr(ip_addr)[0].endswith(settings.ALLOWED_DOMAIN):
                return True
            # If we allow a certain domain and the user is on the server, return the function
            elif socket.gethostbyaddr(ip_addr)[0] =='localhost':
                return True
        except:
            logging.error("Error processing IP address: %s" % str(ip_addr))
            
    return False
    
def login_or_local_required(fn):
    """
        Function decorator to check whether a user is allowed
        to see a view.
    """
    def request_processor(request, *args, **kws):
        if _check_credentials(request):
            return fn(request, *args, **kws)

        # If we made it here, we need to authenticate the user
        redirect_url = reverse('reduction_server.users.views.perform_login')
        redirect_url  += '?next=%s' % request.path
        return redirect(redirect_url)   
    return request_processor

def login_or_local_required_401(fn):
    """
        Function decorator to check whether a user is allowed
        to see a view.
    """
    def request_processor(request, *args, **kws):
        if _check_credentials(request):
            return fn(request, *args, **kws)
        return HttpResponse(status=401)
    return request_processor

def is_instrument_staff(request, instrument_id):
    """
        Determine whether a user is part of an 
        instrument team 
        @param request: HTTP request object
        @param instrument_id: Instrument object
    """
    try:
        instrument_name = str(instrument_id).upper()
        instr_group = Group.objects.get(name="%s%s" % (instrument_name,
                                                       settings.INSTRUMENT_TEAM_SUFFIX))
        if instr_group in request.user.groups.all():
            return True
    except Group.DoesNotExist:
        pass
    return request.user.is_staff

def is_experiment_member(request, instrument, experiment):
    """
        Determine whether a user is part of the given experiment.
        
        @param request: request object
        @param instrument: Instrument name
        @param experiment: IPTS name
    """
    if hasattr(settings, 'HIDE_RUN_DETAILS') and settings.HIDE_RUN_DETAILS is False:
        return True
    
    try:
        if request.user is not None and hasattr(request.user, "ldap_user"):
            groups = request.user.ldap_user.group_names
            return u'sns_%s_team' % str(instrument).lower() in groups \
            or u'sns-ihc' in groups \
            or u'snsadmin' in groups \
            or u'%s' % str(experiment).upper() in groups \
            or is_instrument_staff(request, instrument)
    except:
        logging.error("Error determining whether user %s is part of %s" % (str(request.user), str(experiment)))
    return request.user.is_staff

def monitor(fn):
    """
        Function decorator to monitor page usage
    """
    def request_processor(request, *args, **kws):
        if settings.MONITOR_ON:
            user = None
            if request.user.is_authenticated():
                user = request.user
                
            visit = PageView(user=user,
                             view="%s.%s" % (fn.__module__, fn.__name__),
                             ip=request.META['REMOTE_ADDR'],
                             path=request.path_info)
            visit.save()
        return fn(request, *args, **kws)
    
    return request_processor
