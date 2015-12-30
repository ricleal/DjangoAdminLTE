# Create your tests here.
from django.test import TestCase,  RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import reverse
from django.test.utils import override_settings
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.messages.storage.fallback import FallbackStorage

from .views import list_iptss
'''
Run as:
./manage.py test -k -d
'''

class TestCatalogCalls(TestCase):
    
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user('xxx', 'x@xxx.x', 'xxxx')
        
    def handle_session_and_messages(self,request):
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
    
        
    def test_call_view_denies_anonymous(self):
        response = self.client.get(reverse('catalog:list_instruments'), follow=True)
        self.assertRedirects(response, reverse('users:login')+
                             "?next="+reverse('catalog:list_instruments') )
        response = self.client.post(reverse('catalog:list_iptss', kwargs={'instrument' : 'seq'}), follow=True)
        self.assertRedirects(response, reverse('users:login')+
                             "?next="+reverse('catalog:list_iptss', kwargs={'instrument' : 'seq'}))
 
    def test_call_view_loads(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('index'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/list_instruments.html')
 
    def test_list_iptss_for_mandi(self):
        # Create an instance of a GET request.
        request = self.factory.get(reverse('catalog:list_iptss', kwargs={'instrument' : 'mandi'}))
        request.user = self.user
        self.handle_session_and_messages(request)
        response = list_iptss(request,instrument = 'MANDI')
        self.assertEqual(response.status_code, 200)
        