'''
Created on Feb 4, 2016

@author: rhf

Remote Job Submission API

See: http://www.mantidproject.org/Remote_Job_Submission_API

'''
from django.conf import settings

from pprint import pformat, pprint
from base64 import b64encode

import httplib
import logging
import json

logger = logging.getLogger('remote.fermi')



DEFAULT_REMOTE_DOMAIN = "fermi.ornl.gov"
DEFAULT_REMOTE_PORT = 80

PREFIX = "/MantidRemote"
HEADERS = {"Accept": "application/json"}
TIMEOUT = 5

class Fermi(object):
    '''
    Fermi rest interface
    '''
    def __init__(self, dumper, cookie=None):
        '''
        @param dumper: instance of class that implements IDumper.
            The idea is to have a way to dump errors in django or command line.
        '''
        try:
            self.conn = httplib.HTTPConnection(
                                    settings.REMOTE_DOMAIN,
                                    settings.REMOTE_PORT,
                                    timeout=TIMEOUT)
        except Exception as e:
            # logger.exception(e)
            logger.warning("Using default Fermi configuration. Is there REMOTE_DOMAIN/REMOTE_PORT in the settings?")
            self.conn = httplib.HTTPConnection(
                                    DEFAULT_REMOTE_DOMAIN,
                                    DEFAULT_REMOTE_PORT,
                                    timeout=TIMEOUT)
        
        self.dumper = dumper
        self.headers = HEADERS
        self.set_cookie(cookie)
    
    def set_cookie(self, cookie):
        if cookie:
            self.headers["Cookie"] = cookie
    
    def __del__(self):
        '''
        Just makes sure the HTTP connection will be closed
        '''
        if self.conn is not None:
            self.conn.close()
    
    def _parse_json(self, json_as_string):
        '''
        Makes sure we have a proper json string
        @param json_as_string: must be a string
        @return: python json dictionary in unicode
        '''
        try:
            json_as_dic = json.loads(json_as_string)
            logger.debug("Parsed JSON:\n%s" % pformat(json_as_dic))
            return json_as_dic
        except Exception as e:
            self.dumper.dump_exception(e, "It looks like Fermi did not return a valid JSON:\n%s" % json_as_string)
            return None
    
    def information(self):
        try:
            request_str = '%s/Info' % (PREFIX)
            logger.debug("information: %s" % request_str)
            self.conn.request('GET',
                              request_str,
                              headers=HEADERS)
            response = self.conn.getresponse()
            data_json = self._parse_json(response.read())
            return data_json
        except Exception as e:
            self.dumper.dump_exception(e, "Communication with Fermi server failed.")
            return None
    
    def authentication(self, username, password):
        """
        Autenticate to fermi
        In case of success nothing is returned from fermi, otherwise:
        HTTP/1.1 401 UNAUTHORIZED
        {"Err_Msg": "Authentication failed: Bad username/password combination"}
        
        Sets the cookie
        
        @return: cookie or None if authentication failed
        """
        try:
            userAndPass = b64encode(b"%s:%s" % (username,password)).decode("ascii")
            headers = HEADERS
            headers['Authorization']= 'Basic %s' %  userAndPass
            
            request_str = '%s/authenticate' % (PREFIX)
            logger.debug("information: %s" % request_str)
            self.conn.request('GET',
                              request_str,
                              headers=headers)
            response = self.conn.getresponse()
            if response.status != 200:
                # Only if the authentication fails I have some payload
                data_json = self._parse_json(response.read())
                self.dumper.dump_error(data_json.get("Err_Msg",response.status))
            cookie = response.getheader('set-cookie', None)
            self.set_cookie(cookie)
            return cookie
        except Exception as e:
            self.dumper.dump_exception(e, "Communication with Fermi server failed.")
            return None
        

# Main just for testing
if __name__ == "__main__":
    from server.util.dumper import GeneralDumper
    dumper = GeneralDumper()
    fermi = Fermi(dumper)
    pprint(fermi.information())
    print fermi.authentication("rhf","")
