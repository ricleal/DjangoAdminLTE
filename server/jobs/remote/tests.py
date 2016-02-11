# Create your tests here.
from django.test import TestCase,  RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.storage.fallback import FallbackStorage
from django.test.runner import DiscoverRunner

from . import communication as c

import logging
import getpass
import os
import time

'''
Run as:
./manage.py test -k -d
./manage.py test -k server.jobs.remote.tests

  -k, --keepdb          Preserves the test DB between runs.
  -d, --debug-sql       Prints logged SQL queries on failure.


./manage.py test -k server.jobs.remote.tests.TestRemote.test_stop_transaction

'''



class DebugLoggingTestRunner(DiscoverRunner):
    '''
    Tests by default are not in DEBUG
    Let's get this one in Debug mode
    '''
    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        logger = logging.getLogger('jobs.remote')
        logger.setLevel(logging.DEBUG)
        return super(DebugLoggingTestRunner, self).run_tests(test_labels, extra_tests, **kwargs)


class TestRemote(TestCase):
    '''
    Making methods below classmethod
    to be called only once!
    '''
    
    @classmethod
    def setUpClass(cls):
        cls.factory = RequestFactory()
        cls.request = cls.factory.request()
        cls._handle_session_and_messages()
        cls.cookie = cls._authenticate()
        return super(TestRemote, cls).setUpClass()
    
    @classmethod
    def tearDownClass(cls):
        super(TestRemote, cls).tearDownClass()
    
    @classmethod
    def _handle_session_and_messages(cls):
        setattr(cls.request, 'session', 'session')
        messages = FallbackStorage(cls.request)
        setattr(cls.request, '_messages', messages)
        middleware = SessionMiddleware()
        middleware.process_request(cls.request)
        cls.request.session.save()
    
    @classmethod
    def _authenticate(cls):
        password = getpass.getpass()
        _, cookie = c.authenticate("rhf", password)
        return cookie
    
    def test_authentication(self):
        self.assertFalse(self.cookie is None)
        self.assertIn("sessionid", self.cookie.keys())
    
    def test_start_and_stop_transaction(self):
        
        _, trans_info = c.start_transaction(self.cookie)
        self.assertIn("Directory", trans_info.keys())
        self.assertIn("TransID", trans_info.keys())    
        ## End transaction
        success, _ = c.end_transaction(self.cookie,trans_info["TransID"])
        self.assertTrue(success)
    
    def test_start_and_stop_transaction_upload_download_file(self):
        
        _, trans_info = c.start_transaction(self.cookie)
        self.assertIn("Directory", trans_info.keys())
        self.assertIn("TransID", trans_info.keys())    
        # upload file
        transation_id = trans_info['TransID']
        filename = os.path.join(os.path.dirname(os.path.realpath(__file__)),'test_upload.txt')
        file_content = open(filename,'r')
        success, _ = c.upload(self.cookie, transation_id, {"file1" : file_content})
        self.assertTrue(success)
        
        # download (note the same file name
        _, resp = c.download(self.cookie, transation_id, "file1")
        self.assertTrue(resp is not None)
        self.assertEqual(resp, open(filename,'r').read())
        
        ## End transaction
        success, resp = c.end_transaction(self.cookie,trans_info["TransID"])
        self.assertTrue(success)
    
    def test_start_and_stop_transaction_upload_list_file(self):
        
        _, trans_info = c.start_transaction(self.cookie)
        self.assertIn("Directory", trans_info.keys())
        self.assertIn("TransID", trans_info.keys())    
        # upload file
        transation_id = trans_info['TransID']
        filename = os.path.join(os.path.dirname(os.path.realpath(__file__)),'test_upload.txt')
        file_content = open(filename,'r')
        success, _ = c.upload(self.cookie, transation_id, {"file1" : file_content,"file2" : file_content})
        self.assertTrue(success)
        
        #list file
        _, resp = c.file_listing(self.cookie, transation_id)
        self.assertTrue(resp is not None)
        self.assertIn("Files", resp.keys())
        self.assertIn("file1", resp['Files'])
        self.assertIn("file2", resp['Files'])
        
        ## End transaction
        success, _ = c.end_transaction(self.cookie,trans_info["TransID"])
        self.assertTrue(success)
    
    def test_start_and_stop_transaction_submit_job(self):
        
        _, trans_info = c.start_transaction(self.cookie)
        self.assertIn("Directory", trans_info.keys())
        self.assertIn("TransID", trans_info.keys())    
        #
        transation_id = trans_info['TransID']
        filename = os.path.join(os.path.dirname(os.path.realpath(__file__)),'test_script.py') 
        python_script_dic = {"test_script.py" : str(open(filename,'r').read())}
        _, resp = c.submit_job(self.cookie, transation_id, python_script_dic)
        self.assertIn("JobID", resp.keys())
        job_id = resp["JobID"]
        self.assertNotEqual(job_id, None)
        time.sleep(2)
        
        #list file
        _, resp = c.file_listing(self.cookie, transation_id)
        self.assertTrue(resp is not None)
        self.assertIn("Files", resp.keys())
        self.assertIn("test_script.py", resp['Files'])
        
        ## End transaction
        success, _ = c.end_transaction(self.cookie,trans_info["TransID"])
        self.assertTrue(success)
    
    def test_start_and_stop_transaction_submit_query_job(self):
        
        _, trans_info = c.start_transaction(self.cookie)
        self.assertIn("Directory", trans_info.keys())
        self.assertIn("TransID", trans_info.keys())    
        #
        transation_id = trans_info['TransID']
        filename = os.path.join(os.path.dirname(os.path.realpath(__file__)),'test_script.py') 
        python_script_dic = {"test_script.py" : str(open(filename,'r').read())}
        _, resp = c.submit_job(self.cookie, transation_id, python_script_dic)
        self.assertIn("JobID", resp.keys())
        job_id = resp["JobID"]
        self.assertNotEqual(job_id, None)
        time.sleep(2)
        # query this job:
        _, resp = c.query_job(self.cookie, job_id)
        self.assertNotEqual(resp,None)
        
        # query all jobs:
        _, resp = c.query_job(self.cookie)
        self.assertNotEqual(resp,None)

        ## End transaction
        success, _ = c.end_transaction(self.cookie,transation_id)
        self.assertTrue(success)
    
    def test_start_and_stop_transaction_multiple_submit_query_job(self):
        
        _, trans_info = c.start_transaction(self.cookie)
        self.assertIn("Directory", trans_info.keys())
        self.assertIn("TransID", trans_info.keys())    
        #
        transation_id = trans_info['TransID']
        filename = os.path.join(os.path.dirname(os.path.realpath(__file__)),'test_script.py') 
        python_script_dic = {"test_script.py" : str(open(filename,'r').read())}
        _, resp = c.submit_job(self.cookie, transation_id, python_script_dic)
        self.assertIn("JobID", resp.keys())
        _, resp = c.submit_job(self.cookie, transation_id, python_script_dic)
        self.assertIn("JobID", resp.keys())
        _, resp = c.submit_job(self.cookie, transation_id, python_script_dic)
        self.assertIn("JobID", resp.keys())

        time.sleep(2)
        # query All jobs
        _, resp = c.query_job(self.cookie)
        self.assertNotEqual(resp,None)

        ## End transaction
        success, _ = c.end_transaction(self.cookie,transation_id)
        self.assertTrue(success)
    
    def test_start_and_stop_transaction_submit_query_abort_job(self):
        
        _, trans_info = c.start_transaction(self.cookie)
        self.assertIn("Directory", trans_info.keys())
        self.assertIn("TransID", trans_info.keys())    
        #
        transation_id = trans_info['TransID']
        filename = os.path.join(os.path.dirname(os.path.realpath(__file__)),'test_script.py') 
        python_script_dic = {"test_script.py" : str(open(filename,'r').read())}
        _, resp = c.submit_job(self.cookie, transation_id, python_script_dic)
        self.assertIn("JobID", resp.keys())
        job_id = resp["JobID"]
        self.assertNotEqual(job_id, None)
        success, _ = c.abort_job(self.cookie, job_id)
        self.assertEqual(success,True)
        time.sleep(2)
        # query this job:
        _, resp = c.query_job(self.cookie, job_id)
        self.assertNotEqual(resp,None)
        success, _ = c.abort_job(self.cookie, job_id)
        self.assertEqual(success,False)

        ## End transaction
        success, _ = c.end_transaction(self.cookie,transation_id)
        self.assertTrue(success)