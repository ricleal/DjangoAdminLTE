'''
Created on Feb 4, 2016

@author: rhf

Remote Job Submission API

See: http://www.mantidproject.org/Remote_Job_Submission_API

'''
from django.conf import settings

import requests
import logging

logger = logging.getLogger('jobs.remote')

'''
All function will return to values:
success, value
'''


def authenticate( username,password):
    '''
    Authenticate on Fermi
    @return the cookie
    '''
    try :
        # Verify false, otherwise SSL certicate is invalid
        resp = requests.get(settings.REMOTE_URL +'/authenticate', auth=(username,password), verify=False)
        if resp.ok:
            logger.debug(resp.text)
            return True, resp.cookies.get_dict()
        else:
            logger.error(resp.reason)
            logger.error(resp.text)
            return False, resp.text
    except Exception as e:
        logger.exception(e)
        return False, "Error authenticating with Remote: %s"%str(e)
    
def start_transaction(cookie):
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
            logger.debug(resp.text)
            return True, resp.json()
        else:
            logger.error(resp.reason)
            return False, resp.text
    except Exception as e:
        logger.exception(e)
        return False, "Error starting transaction with Remote: %s"%str(e)

def end_transaction( cookie, transation_id):
    '''
    Need authentication!
    @return: True if succeeded otherwise False
    '''
    try :
        payload = {'Action': 'Stop', 'TransID' : transation_id}
        resp = requests.get(settings.REMOTE_URL +'/transaction', params=payload, verify=False, cookies=cookie)
        if resp.ok:
            logger.info("Stopped Transaction %s."%(transation_id))
            logger.debug(resp.text)
            return True, {}
        else:
            logger.error("Error Stopping Transaction: %s"%resp.reason)
            return False, resp.text
    except Exception as e:
        logger.exception(e)
        return False, "Error stopping transaction with Remote: %s"%str(e)
    

def upload( cookie, transation_id, files):
    '''
    Need authentication!
    @param  files: dictionary of the form:  {'file_name1': open('report.xls', 'rb'),
                                             'file_name2': open('report.txt', 'r'), 
                                             'file_name3': ('report.xls', open('report.xls', 'rb'), 'application/vnd.ms-excel', {'Expires': '0'}),
                                             'file_name4': ('report.csv', 'some,data,to,send\nanother,row,to,send\n')
                                             }
    @return: True if succeeded otherwise False
    '''
    try :
        payload = {'TransID' : transation_id}
        resp = requests.post(settings.REMOTE_URL +'/upload',verify=False, cookies=cookie, data=payload, files=files) #, headers={'Content-Type':' multipart/form-data'})
        if resp.ok:
            logger.info("Uploaded content %s for Transaction %s."%(files.keys(),transation_id))
            return True, {}
        else:
            logger.error("Error Uploading files for Transaction %s: %s"%(transation_id, resp.reason))
            return False, resp.text
    except Exception as e:
        logger.exception(e)
        return False, "Error Uploading files for transaction %s with Remote: %s"%(transation_id,str(e))
    

def download( cookie, transation_id, filename):
    '''
    Need authentication!
    @param filename: Filename in the server 
    @return: the file content or None if error
    '''
    try :
        payload = {'TransID' : transation_id, "File" : filename}
        resp = requests.get(settings.REMOTE_URL +'/download', params=payload, verify=False, cookies=cookie)
        if resp.ok:
            logger.info("Downloaded file %s from Transaction %s."%(filename,transation_id))
            return True, resp.text
        else:
            logger.error("Error Downloading file %s for Transaction %s: %s"%(filename, transation_id, resp.reason))
            return False, resp.text
    except Exception as e:
        logger.exception(e)
        return False, "Error Downloading file %s for transaction %s with Remote: %s"%(filename, transation_id,str(e))
        

def file_listing( cookie, transation_id):
    '''
    Need authentication! 
    @return: { "Files" : [file1, file2, ...]}
    '''
    try :
        payload = {'TransID' : transation_id}
        resp = requests.get(settings.REMOTE_URL +'/files', params=payload, verify=False, cookies=cookie)
        if resp.ok:
            logger.info("Listing files for Transaction %s:\n%s"%(transation_id, resp.text))
            return True, resp.json()
        else:
            logger.error("Error Listing files for Transaction %s: %s"%(transation_id, resp.reason))
            return False, resp.text
    except Exception as e:
        logger.exception(e)
        return False, "Error Listing files for transaction %s with Remote: %s"%(transation_id,str(e))

def submit_job( cookie, transation_id, python_script_dic, job_name=None, number_of_nodes=1, cores_per_node=1):
    '''
    @param  python_script_dic: dictionary of the form:  {'file_name1': open('submit.py', 'r').read()}. Must be single entry!
    @return: {JobID : <job_id> }
    '''
    try :
        script_name, script_content = python_script_dic.items()[0]
        post_payload = {'TransID' : transation_id}
        post_payload["ScriptName"] = script_name
        post_payload[script_name] = script_content 
        post_payload["JobName"] = script_name if job_name is None else job_name
        post_payload["NumNodes"] = number_of_nodes
        post_payload["CoresPerNode"] = cores_per_node
        resp = requests.post(settings.REMOTE_URL +'/submit', data=post_payload, verify=False, cookies=cookie)
        if resp.ok:
            logger.info("Job Submission for Transaction %s:\n%s"%(transation_id,resp.text))
            return True, resp.json()
        else:
            logger.error("Error Job Submission for Transaction %s: %s"%(transation_id, resp.reason))
            return False, resp.text
    except Exception as e:
        logger.exception(e)
        return False, "Error Job Submission for transaction %s with Remote: %s"%(transation_id,str(e))


def query_job( cookie, job_id=None):
    '''
    @param  job_id : if None query all jobs, otherwise query for the job_id given
    JobStatus: RUNNING, QUEUED, COMPLETED, REMOVED, DEFERRED, IDLE or UNKNOWN
    @return:
        {  
          "43015": {
            "CompletionDate": "2016-02-08T17:03:07+00:00", 
            "StartDate": "2016-02-08T17:03:06+00:00", 
            "SubmitDate": "2016-02-08T17:03:06+00:00", 
            "JobName": "test_script.py", 
            "ScriptName": "test_script.py", 
            "JobStatus": "COMPLETED", 
            "TransID": 555
          }, 
          "43025": {
            "CompletionDate": "2016-02-08T17:07:58+00:00", 
            "StartDate": "2016-02-08T17:07:57+00:00", 
            "SubmitDate": "2016-02-08T17:07:57+00:00", 
            "JobName": "test_script.py", 
            "ScriptName": "test_script.py", 
            "JobStatus": "COMPLETED", 
            "TransID": 556
          },
          (..................)
        }
    '''
    try :
        payload = {'JobID' : job_id} if job_id else None
        resp = requests.get(settings.REMOTE_URL +'/query', params=payload, verify=False, cookies=cookie)
        if resp.ok:
            logger.debug("Query Job %s:\n%s"%(job_id, resp.text))
            return True, resp.json()
        else:
            logger.error("Error Job Query %s: %s"%(job_id, resp.reason))
            return False, resp.text
    except Exception as e:
        logger.exception(e)
        return False, "Error Query Job %s with Remote: %s"%(job_id,str(e))


def get_job_status( cookie, job_id):
    '''
    Facade for the method query_job
    '''
    resp =  query_job( cookie, job_id)
    if resp is not None and len(resp.items()) == 1:
        job_details =  resp.values()[0]
        return True, job_details["JobStatus"]
    else:
        return False, "get_job_status did not get the expected result: %s"%resp
        

def abort_job( cookie, job_id):
    '''
    @return: True if succeeded otherwise False
    '''
    try :
        payload = {'JobID' : job_id}
        resp = requests.get(settings.REMOTE_URL +'/abort', params=payload, verify=False, cookies=cookie)
        if resp.ok:
            logger.debug("Job aborted successfully %s."%(job_id))
            return True, resp.json()
        else:
            logger.error("Error Job Abort %s: %s"%(job_id, resp.reason))
            return False, resp.text
    except Exception as e:
        logger.exception(e)
        return False, "Error Job Abort %s with Remote: %s"%(job_id,str(e))
