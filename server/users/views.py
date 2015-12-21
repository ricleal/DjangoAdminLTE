"""
    User management
"""
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth import login, logout, authenticate
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.signals import user_logged_in


def perform_login(request):
    """
        Perform user authentication
    """
    user = None

    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None and not user.is_anonymous():
            login(request, user)
        else:
            messages.error(request, "Invalid username or password!")

    if request.user.is_authenticated():
        # If we came from a given page and just needed
        # authentication, go back to that page.
        if "next" in request.GET:
            redirect_url = request.GET["next"]
            return redirect(redirect_url)
        return redirect(reverse('index'))
    else:
        return render_to_response('users/login.html', {},
                              context_instance=RequestContext(request))

def perform_logout(request):
    """
        Logout user
    """
    logout(request)
    return redirect(reverse("index"))
