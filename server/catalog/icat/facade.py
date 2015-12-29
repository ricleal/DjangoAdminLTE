from django.utils import dateparse
from django.contrib import messages

from .communication import IDumper, ICat

import json
import logging


logger = logging.getLogger('catalog.icat')

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

    def dump_exception(self, exception, message):
        """
        @param exception: Must be a valid python exception
        @param message: Must be a string
        """
        logger.exception(exception)
        logger.error(message)
        messages.error(self.django_request, message)
        messages.error(self.django_request, str(exception))

    def dump_error(self, message):
        """
        @param message: Must be a string
        """
        logger.error(message)
        messages.error(self.django_request, message)

class Catalog(object):
    '''
    Custom functionality to ICAT!
    '''
    def __init__(self, request):
        '''
        @param dumper: instance of class that implements IDumper.
            The idea is to have a way to dump errors in django or command line.
        '''
        self.dumper = DjangoDumper(request)
        self.icat = icat = ICat(self.dumper)

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

    def _substitute_keys_in_dictionary(self,obj,old_key,new_key):
        '''
        @param obj : can be nested dict or list of dicts, etc:
        '''
        if isinstance(obj, dict):
            if obj.has_key(old_key):
                obj[new_key]=obj.pop(old_key)
                #obj[new_key] = obj[old_key]
                #obj.pop(old_key)
            return {k: self._substitute_keys_in_dictionary(v,old_key,new_key) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._substitute_keys_in_dictionary(elem,old_key,new_key) for elem in obj]

    def _convert_to_datetime(self,obj,key):
        '''
        @param obj : can be nested dict or list of dicts, etc:
        @param key : a key to convest str value to datetime
        '''
        if isinstance(obj, dict):
            if obj.has_key(key):
                obj[key] = dateparse.parse_datetime(obj[key])
            return {k: self._convert_to_datetime(v,key) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._convert_to_datetime(elem,key) for elem in obj]

    def get_instruments(self):
        '''
        @return:
        [u'ARCS',
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
                 u'VULCAN']
        '''

        data_json = self.icat.get_instruments()
        if data_json is not None and data_json.has_key('instrument'):
            return data_json['instrument']
        else:
            self.dumper.dump_error("ICAT did not return the expected result....")
            return None

    def get_experiments_meta(self, instrument):
        '''
        @param instrument: Valid instrument as string
        @return:
              [{u'@id': u'IPTS-2774',
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
                u'title': u'CaRuTiO; T=4K; Ei=120 meV; Fch1=300 Hz T0=90 Hz'}]
        '''

        json_data = self.icat.get_experiments_meta(instrument)
        if json_data is not None and json_data.has_key('proposal'):
            json_data = json_data['proposal']
        else:
            self.dumper.dump_error("ICAT did not return the expected result. Is the instrument valid?")
            return None
        self._substitute_keys_in_dictionary(json_data,'@id','id')
        self._convert_to_datetime(json_data,'createTime')
        return json_data;

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

        json_data = self.icat.get_runs_all(instrument, experiment)
        self._substitute_keys_in_dictionary(json_data,'@id','id')
        self._convert_to_datetime(json_data,'createTime')
        self._convert_to_datetime(json_data,'endTime')
        self._convert_to_datetime(json_data,'startTime')
        return json_data;

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
            raw_ranges = self.icat.get_run_ranges(instrument, experiment)
            if raw_ranges is not None and raw_ranges.has_key('runRange'):
                ranges = self._hyphen_range(raw_ranges["runRange"])
            else:
                self.dumper.dump_error("ICAT did not return the expected result....")
                return None
            return json.loads("[" + ranges + "]")

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
        raw_ranges = self.icat.get_run_ranges_meta(instrument, experiment)
        ranges = self._hyphen_range(raw_ranges["proposal"]["runRange"])
        raw_ranges["proposal"]["runRange"] = json.loads("[" + ranges + "]")
        return raw_ranges
