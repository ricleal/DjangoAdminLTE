'''
Created on Feb 4, 2016

@author: rhf

Remote Job Submission API

See: http://www.mantidproject.org/Remote_Job_Submission_API

'''
from django.conf import settings
from django.contrib import messages

import requests


from pprint import pformat, pprint
from base64 import b64encode

import httplib
import logging

logger = logging.getLogger('jobs.remote')


def authenticate(request, username,password):
    '''
    Authenticate on Fermi
    @return the cookie
    '''
    try :
        # Verify false, otherwise SSL certicate is invalid
        resp = requests.get(settings.REMOTE_URL +'/authenticate', auth=(username,password), verify=False)
        if not resp.OK:
            messages.error(request, resp.text)
        else:
            return resp.cookies['sessionid']
    except Exception as e:
        logger.exception(e)
    return None
    
def start_transaction(request, cookie):
    '''
    Need authentication!
    Fermi returns:
    {
        "Directory": "/lustre/snsfs/scratch/apache/rhf_535",
        "TransID": 535
    }
    @return: http code, payload,
    '''
    try :
        # Verify false, otherwise SSL certicate is invalid
        resp = requests.get(settings.REMOTE_URL +'/transaction?Action=Start',  cookies=cookies)
        if not resp.OK:
            messages.error(request, resp.text)
        else:
            return resp.cookies['sessionid']
    except Exception as e:
        logger.exception(e)
    return None

    try:
        request_str = '%s/transaction?Action=Start' % (PREFIX)
        logger.debug("transaction: %s" % request_str)
        self.conn.request('GET',
                          request_str,
                          headers=self.headers)
        response = self.conn.getresponse()
        return response.status, response.read()
    except Exception as e:
        self.dumper.dump_exception(e, "Communication with Fermi server failed.")
        return None
    
        
