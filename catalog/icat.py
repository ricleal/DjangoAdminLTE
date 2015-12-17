'''
Created on Dec 8, 2015

@author: rhf
'''

import httplib
import json
import logging

from django.conf import settings
from django.contrib import messages
from abc import ABCMeta, abstractmethod
from pprint import pformat, pprint
from django.utils import dateparse

"""

ICAT Json interface

"""


logger = logging.getLogger('catalog.icat')

# Defaults:
DEFAULT_ICAT_DOMAIN = "icat.sns.gov"
DEFAULT_ICAT_PORT = 2080

TIMEOUT = 3
HEADERS = {"Accept": "application/json"}

class IDumper():
    __metaclass__ = ABCMeta

    @abstractmethod
    def dump_error(self, exception, message):
        raise NotImplementedError

class DjangoDumper(IDumper):
    """
    For Django
    If using django, instantiatiate this class first with:
    dumper = DjangoDumper(request)
    Then instantiate ICat
    icat = ICat(dumper)
    This will allow passing messages to the interface
    """
    def __init__(self, django_request):
        self.django_request = django_request

    def dump_error(self, exception, message):
        """
        @param exception: Must be a valid python exception
        @param message: Must be a string
        """
        logger.exception(exception)
        logger.error(message)
        messages.error(self.django_request, message)
        messages.error(self.django_request, str(exception))

class GeneralDumper(IDumper):
    """
    For Command Line Testing.
    If running outside Django it overrides the logger.
    Use as:
    dumper = GeneralDumper(request)
    icat = ICat(dumper)
    """
    def __init__(self):
        # overrides logger
        global logger
        logging.basicConfig(level=logging.DEBUG)
        logger = logging.getLogger(__name__)

    def dump_error(self, exception, message):
        """
        @param exception: Must be a valid python exception
        @param message: Must be a string
        """
        logger.exception(exception)
        logger.error(message)

class ICat(object):
    '''
    ICAT rest interface
    '''
    def __init__(self, dumper, facility="SNS"):
        '''
        @param dumper: instance of class that implements IDumper.
            The idea is to have a way to dump errors in django or command line.
        '''
        try:
            self.conn = httplib.HTTPConnection(
                                    settings.ICAT_DOMAIN,
                                    settings.ICAT_PORT,
                                    timeout=TIMEOUT)
        except Exception as e:
            # logger.exception(e)
            logger.warning("Using default icat configuration. Is there ICAT_DOMAIN/ICAT_PORT in the settings?")
            self.conn = httplib.HTTPConnection(
                                    DEFAULT_ICAT_DOMAIN,
                                    DEFAULT_ICAT_PORT,
                                    timeout=TIMEOUT)
        self.facility = facility
        self.dumper = dumper

    def __del__(self):
        '''
        Just makes sure the HTTP connection will be closed
        '''
        if self.conn is not None:
            logger.debug("Closing ICAT HTTP connection...")
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
            self.dumper.dump_error(e, "It looks like ICAT did not return a valid JSON:\n%s" % json_as_string)
            return None

    @staticmethod
    def _hyphen_range(s):
        """ Takes a range in form of "a-b" and generate a list of numbers between a and b inclusive.
        Also accepts comma separated ranges like "a-b,c-d,f" will build a list which will include
        Numbers from a to b, a to d and f"""
        s = "".join(s.split())  # removes white space
        r = set()
        for x in s.split(','):
            t = x.split('-')
            if len(t) not in [1, 2]:
                logger.error("hash_range is given its arguement as " + s + " which seems not correctly formated.")
            r.add(int(t[0])) if len(t) == 1 else r.update(set(range(int(t[0]), int(t[1]) + 1)))
        l = list(r)
        l.sort()
        l_in_str = ','.join(str(x) for x in l)
        return l_in_str

    @staticmethod
    def _substitute_keys_in_dictionary(list_of_dicts,old_key,new_key):
        for d in list_of_dicts:
            d[new_key]=d.pop(old_key)

    @staticmethod
    def _convert_to_datetime(list_of_dicts,key):
        for d in list_of_dicts:
            d[key] = dateparse.parse_datetime(d[key])

    def get_instruments(self):
        '''
        @return:
        {u'instrument': [u'ARCS',
                 u'BSS',
                 u'CNCS',
                 u'CORELLI',
                 u'EQSANS',
                 u'FNPB',
                 u'HYS',
                 u'HYSA',
                 u'MANDI',
                 u'NOM',
                 u'NSE',
                 u'PG3',
                 u'REF_L',
                 u'REF_M',
                 u'SEQ',
                 u'SNAP',
                 u'TOPAZ',
                 u'USANS',
                 u'VIS',
                 u'VULCAN']}
        '''

        try:
            request_str = '/icat-rest-ws/experiment/%s' % (self.facility)
            logger.debug("get_instruments: %s" % request_str)
            self.conn.request('GET',
                              request_str,
                              headers=HEADERS)
            response = self.conn.getresponse()
            return self._parse_json(response.read())
        except Exception as e:
            self.dumper.dump_error(e, "Communication with ICAT server failed.")
            return None

    def get_experiments(self, instrument):
        '''
        @param instrument: Valid instrument as string
        @return:
        {u'proposal': [u'2009_2_17_SCI',
               u'2009_3_17_SCI',
               u'2010_2_17_SCI',
                (..........................)
               u'IPTS-9650',
               u'IPTS-9655',
               u'IPTS-9772',
               u'IPTS-9817',
               u'IPTS-9830',
               u'IPTS-9868']}
        '''

        try:
            request_str = '/icat-rest-ws/experiment/%s/%s' % (self.facility, instrument)
            logger.debug("get_experiments: %s" % request_str)
            self.conn.request('GET',
                              request_str,
                              headers=HEADERS)
            response = self.conn.getresponse()
            return self._parse_json(response.read())
        except Exception as e:
            self.dumper.dump_error(e, "Communication with ICAT server failed.")
            return None

    def get_experiments_meta(self, instrument):
        '''
        @param instrument: Valid instrument as string
        @return:
            {u'proposal': [{u'@id': u'IPTS-2774',
                u'collection': u'12',
                u'createTime': u'2012-08-02T16:19:37.604-04:00',
                u'title': u'Junk run'},
               {u'@id': u'IPTS-2911',
                u'collection': u'0',
                u'createTime': u'2012-08-01T20:17:26.894-04:00',
                u'title': u'H2O%2DMCM%2D41%2C cooling%2C T%3D%7E230 K Ei%3D800 meV F1%40600 T0%40150'},
                (.......................)
               {u'@id': u'IPTS-14252',
                u'collection': u'0',
                u'createTime': u'2015-12-15T15:53:34.576-05:00',
                u'title': u'CaRuTiO; T=4K; Ei=120 meV; Fch1=300 Hz T0=90 Hz'}]}
        '''

        try:
            request_str = '/icat-rest-ws/experiment/%s/%s/meta' % (self.facility, instrument)
            logger.debug("get_experiments: %s" % request_str)
            self.conn.request('GET',
                              request_str,
                              headers=HEADERS)
            response = self.conn.getresponse()
            json_data = self._parse_json(response.read())
            self._substitute_keys_in_dictionary(json_data['proposal'],'@id','id')
            self._convert_to_datetime(json_data['proposal'],'createTime')
            return json_data;
        except Exception as e:
            self.dumper.dump_error(e, "Communication with ICAT server failed.")
            return None

    def get_user_experiments(self, ucams_uid):
        '''
        @param ucams_uid: valid 3 characters ORNL ucams user uid
        @param instrument: Valid instrument as string
        @return:
        {
            "proposals": [
                {
                    "IPTS": 522
                },
                {
                    "IPTS": 1602
                },
                (.....................)
                {
                    "IPTS": 15834
                }
            ]
        }
        '''

        try:
            request_str = '/prpsl_ws/getProposalNumbersByUser/%s' % (ucams_uid)
            logger.debug("get_user_experiments: %s" % request_str)
            self.conn.request('GET',
                              request_str,
                              headers=HEADERS)
            response = self.conn.getresponse()
            return self._parse_json(response.read())
        except Exception as e:
            self.dumper.dump_error(e, "Communication with ICAT server failed.")
            return None

    def get_run_ranges(self, instrument, experiment):
        '''
        @param instrument: Valid instrument as string
        @return:
        {u'runRange': u'40136-40174, 40211-40246, 42375-42403'}
        '''

        try:
            request_str = '/icat-rest-ws/experiment/%s/%s/%s' % (
                                                     self.facility,
                                                     instrument,
                                                     experiment)
            logger.debug("get_run_ranges: %s" % request_str)
            self.conn.request('GET',
                              request_str,
                              headers=HEADERS)
            response = self.conn.getresponse()
            return self._parse_json(response.read())
        except Exception as e:
            self.dumper.dump_error(e, "Communication with ICAT server failed.")
            return None



    def get_runs(self, instrument, experiment):
        """
        Similar to get_run_ranges
        But returns:
        @return:
        {u'runRange': [40136,
               40137,
               (.........................)
               42396,
               42397,
               42398,
               42399,
               42400,
               42401,
               42402,
               42403]}
        """
        raw_ranges = self.get_run_ranges(instrument, experiment)
        ranges = self._hyphen_range(raw_ranges["runRange"])
        raw_ranges["runRange"] = self._parse_json("[" + ranges + "]")
        return raw_ranges

    def get_run_ranges_meta(self, instrument, experiment):
        '''
        @param instrument: Valid instrument as string
        @return:
        {
            "proposal": {
                "@id": "IPTS-8776",
                "collection": "0",
                "createTime": "2014-08-22T17:27:17.588-04:00",
                "runRange": "990-1002, 1005-1006, 1008-1025, 1027-1040, 1091-1155, 1157-3859, 3894-3901, 4339-4354, 4356-4381, 4389-4391",
                "title": "Test Run-73. 1857"
            }
        }
        '''

        try:
            request_str = '/icat-rest-ws/experiment/%s/%s/%s/meta' % (
                                                     self.facility,
                                                     instrument,
                                                     experiment)
            logger.debug("get_run_ranges_meta: %s" % request_str)
            self.conn.request('GET',
                              request_str,
                              headers=HEADERS)
            response = self.conn.getresponse()
            return self._parse_json(response.read())
        except Exception as e:
            self.dumper.dump_error(e, "Communication with ICAT server failed.")
            return None

    def get_runs_meta(self, instrument, experiment):
        """
        Similar to get_run_ranges_meta but with runs as list
        But returns:
        @return:
        {u'proposal': {u'@id': u'IPTS-9868',
                       u'createTime': u'2013-08-19T18:58:56.688-04:00',
                       u'runRange': [40136,
                                     40137,
                                     40138,
                                     (..................)
                                     42400,
                                     42401,
                                     42402,
                                     42403],
                       u'title': u'Vanadium 5x5 White beam><E=110meV, T0=150Hz, Att1\n slitPacks: FC1=SEQ-700-3.5-AST FC2=SEQ-100-2.0-AST'}}
        """
        raw_ranges = self.get_run_ranges_meta(instrument, experiment)
        ranges = self._hyphen_range(raw_ranges["proposal"]["runRange"])
        raw_ranges["proposal"]["runRange"] = self._parse_json("[" + ranges + "]")
        return raw_ranges

    def get_runs_all(self, instrument, experiment):
        '''
        @param instrument: Valid instrument as string
        @return:
        {u'proposal': {u'@id': u'IPTS-9868',
               u'createTime': u'2013-08-19T18:58:56.688-04:00',
               u'runs': {u'run': [{u'@id': u'40136',
                                   u'duration': u'636.419',
                                   u'endTime': u'2013-08-19T18:58:53.298-04:00',
                                   u'startTime': u'2013-08-19T18:48:16.879-04:00',
                                   u'totalCounts': u'1.9907726E7'},
                                  {u'@id': u'40137',
                                   u'duration': u'9409.68',
                                   u'endTime': u'2013-08-20T11:20:58.309-04:00',
                                   u'startTime': u'2013-08-20T08:44:08.632-04:00',
                                   u'totalCounts': u'16740.0'},
                                 (................................)
                                  {u'@id': u'42401',
                                   u'duration': u'3028.77',
                                   u'endTime': u'2013-09-30T23:12:06.482-04:00',
                                   u'protonCharge': u'4.00066404949e+12',
                                   u'startTime': u'2013-09-30T22:21:37.715-04:00',
                                   u'totalCounts': u'6920258.0'},
                                  {u'@id': u'42402',
                                   u'duration': u'3177.77',
                                   u'endTime': u'2013-10-01T00:17:07.565-04:00',
                                   u'protonCharge': u'3.02740097175e+12',
                                   u'startTime': u'2013-09-30T23:24:09.798-04:00',
                                   u'totalCounts': u'8093002.0'},
                                  {u'@id': u'42403',
                                   u'duration': u'34757.0',
                                   u'endTime': u'2013-10-01T10:07:16.126-04:00',
                                   u'startTime': u'2013-10-01T00:27:59.082-04:00',
                                   u'totalCounts': u'129560.0'}]},
               u'title': u'Vanadium 5x5 White beam><E=110meV, T0=150Hz, Att1\n slitPacks: FC1=SEQ-700-3.5-AST FC2=SEQ-100-2.0-AST'}}
        '''

        try:
            request_str = '/icat-rest-ws/experiment/%s/%s/%s/all' % (
                                                     self.facility,
                                                     instrument,
                                                     experiment)
            logger.debug("get_runs_all: %s" % request_str)
            self.conn.request('GET',
                              request_str,
                              headers=HEADERS)
            response = self.conn.getresponse()
            return self._parse_json(response.read())
        except Exception as e:
            self.dumper.dump_error(e, "Communication with ICAT server failed.")
            return None

    def get_run_info(self, instrument, run_number):
        '''
        @param instrument: Valid instrument as string
        @return:
        {u'complete': u'false',
         u'duration': u'3028.77',
         u'endTime': u'2013-09-30T23:12:06.482-04:00',
         u'locations': {u'location': [u'/SNS/SEQ/IPTS-9868/shared/autoreduce/reduction_log/SEQ_42401.nxs.h5.log',
                                      u'/SNS/SEQ/IPTS-9868/shared/autoreduce/SEQ_42401_autoreduced.nxspe',
                                      u'/SNS/SEQ/IPTS-9868/shared/autoreduce/SEQ_42401_autoreduced.nxs',
                                      u'/SNS/SEQ/IPTS-9868/nexus/SEQ_42401.nxs.h5',
                                      u'/SNS/SEQ/IPTS-9868/adara/SEQ_42401.adara']},
         u'proposal': u'IPTS-9868',
         u'protonCharge': u'4.00066404949e+12',
         u'startTime': u'2013-09-30T22:21:37.715-04:00',
         u'totalCounts': u'6920258.0'}
        '''

        try:
            request_str = '/icat-rest-ws/dataset/%s/%s/%s' % (
                                                     self.facility,
                                                     instrument,
                                                     run_number)
            logger.debug("get_run_info: %s" % request_str)
            self.conn.request('GET',
                              request_str,
                              headers=HEADERS)
            response = self.conn.getresponse()
            return self._parse_json(response.read())
        except Exception as e:
            self.dumper.dump_error(e, "Communication with ICAT server failed.")
            return None

    def get_run_info_meta_only(self, instrument, run_number):
        '''
        @param instrument: Valid instrument as string
        @return:
        {u'complete': u'false',
         u'duration': u'3028.77',
         u'endTime': u'2013-09-30T23:12:06.482-04:00',
         u'proposal': u'IPTS-9868',
         u'protonCharge': u'4.00066404949e+12',
         u'startTime': u'2013-09-30T22:21:37.715-04:00',
         u'totalCounts': u'6920258.0'}
        '''

        try:
            request_str = '/icat-rest-ws/dataset/%s/%s/%s/metaOnly' % (
                                                     self.facility,
                                                     instrument,
                                                     run_number)
            logger.debug("get_run_info_meta_only: %s" % request_str)
            self.conn.request('GET',
                              request_str,
                              headers=HEADERS)
            response = self.conn.getresponse()
            return self._parse_json(response.read())
        except Exception as e:
            self.dumper.dump_error(e, "Communication with ICAT server failed.")
            return None

    def get_run_info_lite(self, instrument, run_number):
        '''
        @param instrument: Valid instrument as string
        @return:
        {u'complete': u'false',
         u'duration': u'3028.77',
         u'endTime': u'2013-09-30T23:12:06.482-04:00',
         u'locations': {u'location': [u'/SNS/SEQ/IPTS-9868/adara/SEQ_42401.adara',
                                      u'/SNS/SEQ/IPTS-9868/nexus/SEQ_42401.nxs.h5',
                                      u'/SNS/SEQ/IPTS-9868/shared/autoreduce/reduction_log/SEQ_42401.nxs.h5.log',
                                      u'/SNS/SEQ/IPTS-9868/shared/autoreduce/SEQ_42401_autoreduced.nxs',
                                      u'/SNS/SEQ/IPTS-9868/shared/autoreduce/SEQ_42401_autoreduced.nxspe']},
         u'proposal': u'IPTS-9868',
         u'protonCharge': u'4.00066404949e+12',
         u'startTime': u'2013-09-30T22:21:37.715-04:00',
         u'totalCounts': u'6920258.0'}
        '''

        try:
            request_str = '/icat-rest-ws/dataset/%s/%s/%s/lite' % (
                                                     self.facility,
                                                     instrument,
                                                     run_number)
            logger.debug("get_run_info_lite: %s" % request_str)
            self.conn.request('GET',
                              request_str,
                              headers=HEADERS)
            response = self.conn.getresponse()
            return self._parse_json(response.read())
        except Exception as e:
            self.dumper.dump_error(e, "Communication with ICAT server failed.")
            return None

    def get_last_run(self, instrument):
        '''
        Gets the last run mumber for a certain instrument
        @param instrument: Valid instrument as string
        @return:
        {u'number': u'13780'}
        '''

        try:
            request_str = '/icat-rest-ws/datafile/%s/%s' % (self.facility, instrument)
            logger.debug("get_last_run: %s" % request_str)
            self.conn.request('GET',
                              request_str,
                              headers=HEADERS)
            response = self.conn.getresponse()
            return self._parse_json(response.read())
        except Exception as e:
            self.dumper.dump_error(e, "Communication with ICAT server failed.")
            return None

    def get_run_files(self, instrument, run_number):
        '''
        @param instrument: Valid instrument as string
        @return:
        {u'location': [u'/SNS/SEQ/IPTS-9868/adara/SEQ_42401.adara',
               u'/SNS/SEQ/IPTS-9868/nexus/SEQ_42401.nxs.h5',
               u'/SNS/SEQ/IPTS-9868/shared/autoreduce/reduction_log/SEQ_42401.nxs.h5.log',
               u'/SNS/SEQ/IPTS-9868/shared/autoreduce/SEQ_42401_autoreduced.nxs',
               u'/SNS/SEQ/IPTS-9868/shared/autoreduce/SEQ_42401_autoreduced.nxspe']}
        '''

        try:
            request_str = '/icat-rest-ws/datafile/%s/%s/%s' % (
                                                     self.facility,
                                                     instrument,
                                                     run_number)
            logger.debug("get_run_info: %s" % request_str)
            self.conn.request('GET',
                              request_str,
                              headers=HEADERS)
            response = self.conn.getresponse()
            return self._parse_json(response.read())
        except Exception as e:
            self.dumper.dump_error(e, "Communication with ICAT server failed.")
            return None


# Main just for testing
if __name__ == "__main__":

    dumper = GeneralDumper()
    icat = ICat(dumper)
    pprint(icat.get_instruments())
    pprint(icat.get_experiments("SEQ"))
    pprint(icat.get_experiments_meta("SEQ"))
    pprint(icat.get_run_ranges("SEQ", 'IPTS-9868'))
    pprint(icat.get_runs("SEQ", 'IPTS-9868'))
    pprint(icat.get_run_ranges_meta("SEQ", 'IPTS-9868'))
    pprint(icat.get_runs_meta("SEQ", 'IPTS-9868'))
    pprint(icat.get_runs_all("SEQ", 'IPTS-9868'))
    pprint(icat.get_run_info("SEQ", '42401'))
    pprint(icat.get_run_info_meta_only("SEQ", '42401'))
    pprint(icat.get_run_info_lite("SEQ", '42401'))
    pprint(icat.get_last_run("TOPAZ"))
    pprint(icat.get_run_files("SEQ", '42401'))
    pprint(icat.get_user_experiments('19g'))
