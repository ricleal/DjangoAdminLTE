# Create your tests here.
from django.test import TestCase,  RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.storage.fallback import FallbackStorage

from . import communication as c

import getpass

'''
Run as:
./manage.py test -k -d
./manage.py test -k server.jobs.remote.tests

  -k, --keepdb          Preserves the test DB between runs.
  -d, --debug-sql       Prints logged SQL queries on failure.


./manage.py test -k server.jobs.remote.tests.TestRemote.test_stop_transaction

'''


class TestRemote(TestCase):
    
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.request = self.factory.request()
        self._handle_session_and_messages()
        self.cookie = self._authenticate()
        
    def _handle_session_and_messages(self):
        setattr(self.request, 'session', 'session')
        messages = FallbackStorage(self.request)
        setattr(self.request, '_messages', messages)
        middleware = SessionMiddleware()
        middleware.process_request(self.request)
        self.request.session.save()
    
    def _authenticate(self):
        password = getpass.getpass()
        cookie = c.authenticate(self.request, "rhf", password)
        return cookie
    
    def test_authentication(self):
        self.assertFalse(self.cookie is None)
        self.assertIn("sessionid", self.cookie.keys())
    
    def test_start_and_stop_transaction(self):
        
        trans_info = c.start_transaction(self.request, self.cookie)
        self.assertIn("Directory", trans_info.keys())
        self.assertIn("TransID", trans_info.keys())    
        ## End transaction
        resp = c.end_transaction(self.request, self.cookie,trans_info["TransID"])
        self.assertTrue(resp)
    
    
    
    
            