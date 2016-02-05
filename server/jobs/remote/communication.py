'''
Created on Feb 4, 2016

@author: rhf

Remote Job Submission API

See: http://www.mantidproject.org/Remote_Job_Submission_API

'''
from django.conf import settings
from django.contrib import messages

import requests
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
        if resp.ok:
            return resp.cookies.get_dict()
        else:
            logger.error(resp.reason)
            logger.error(resp.text)
            messages.error(request, resp.text)
    except Exception as e:
        logger.exception(e)
        messages.error(request, "Error authenticating with Remote: %s"%str(e))
    return None
    
def start_transaction(request, cookie):
    '''
    Need authentication!
    
    @return: None or
    {
        "Directory": "/lustre/snsfs/scratch/apache/rhf_535",
        "TransID": 535
    }
    '''
    try :
        payload = {'Action': 'Start'}
        resp = requests.get(settings.REMOTE_URL +'/transaction', params=payload, verify=False, cookies=cookie)
        if resp.ok:
            logger.info("Started Transaction: %s"%(resp.text))
            return resp.json()
        else:
            logger.error(resp.reason)
            messages.error(request, resp.text)
    except Exception as e:
        logger.exception(e)
        messages.error(request, "Error starting transaction with Remote: %s"%str(e))
    return None

def end_transaction(request, cookie, transation_id):
    '''
    Need authentication!
    @return: True if ended transaction
    '''
    try :
        payload = {'Action': 'Stop', 'TransID' : transation_id}
        resp = requests.get(settings.REMOTE_URL +'/transaction', params=payload, verify=False, cookies=cookie)
        if resp.ok:
            logger.info("Stopped Transaction %s."%(transation_id))
            return True
        else:
            logger.error("Error Stopping Transaction: %s"%resp.reason)
            messages.error(request, resp.text)
    except Exception as e:
        logger.exception(e)
        messages.error(request, "Error stopping transaction with Remote: %s"%str(e))
    return False



