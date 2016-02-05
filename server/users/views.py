"""
    User management
"""
from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME, authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import CreateView, UpdateView, FormView, RedirectView
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

import logging
import json

from .models import UserProfile
from server.jobs.remote import communication as fermi

logger = logging.getLogger('users')

class LoginView(FormView):
    """
    
    """
    form_class = AuthenticationForm
    template_name = 'users/login.html'
    redirect_field_name = REDIRECT_FIELD_NAME
    success_url = reverse_lazy('index')
    create_profile_url = reverse_lazy('users:profile_create')
    
    def _remote_authentication(self, request, username, password):
        """
        remote authentication to fermi
        Sets a cookie for fermi
        """
        cookie = fermi.authenticate(request, username, password)
        if cookie:
            request.session['remote']=cookie
    
    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Mathieu athentication
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
#         user = authenticate(username=username, password=password)
#         if user is not None and not user.is_anonymous():
#             auth_login(self.request, user)
#         else:
#             messages.error(self.request, "Django Authenticate Failed. Invalid username or password!")
        
        # Default authentication
        auth_login(self.request, form.get_user())
        # Fermi
        self._remote_authentication(self.request, username, password)
        
        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        try:
            UserProfile.objects.get(user__username = self.request.user)
        except ObjectDoesNotExist:
            logger.info("Redirecting to create user profile!")
            return self.create_profile_url

        redirect_to = self.request.GET.get(self.redirect_field_name,'/')
        if not is_safe_url(url=redirect_to, host=self.request.get_host()):
            redirect_to = self.success_url
        return redirect_to
    
    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password!")
        return super(LoginView, self).form_invalid(form)

class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """
    url = reverse_lazy('users:login')

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        response = super(LogoutView, self).get(request, *args, **kwargs)
        response.delete_cookie('remote')
        return response


class ProfileUpdate(LoginRequiredMixin,SuccessMessageMixin,UpdateView):
    model = UserProfile
    fields = ['instrument','home_institution']
    success_url = reverse_lazy('index')
    success_message = "Your profile was updated successfully."
    
class ProfileCreate(LoginRequiredMixin,SuccessMessageMixin,CreateView):
    model = UserProfile
    fields = ['instrument','home_institution']
    success_url = reverse_lazy('index')
    success_message = "Your profile was created successfully."
    
    def form_valid(self, form):
        '''
        Add user to the form as it is not shown to the user
        '''
        user = self.request.user
        form.instance.user = user
        return super(ProfileCreate, self).form_valid(form)
     
@login_required
def get_users_json(request):
    """
    Ajax call to get all the possible users
    @return: Json in DataTables format :
    {
  "data": [
    [
      "col 1 row 1",
      "col 2 row 1",
      ],[...]
      ] }
    
    """
    users_queryset = get_user_model().objects.all()
    users_json = {"data" : [ [user.username,user.fullname] for user in users_queryset] }
    response = JsonResponse(users_json, safe=False)
    return response
