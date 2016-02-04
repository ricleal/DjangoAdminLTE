'''
Created on Feb 4, 2016

@author: rhf
'''
from django.contrib import messages

from abc import ABCMeta, abstractmethod
from pprint import pprint

import logging

logger = logging.getLogger('util.dumper')

class IDumper():
    __metaclass__ = ABCMeta

    @abstractmethod
    def dump_exception(self, exception, message):
        raise NotImplementedError

    @abstractmethod
    def dump_error(self, message):
        raise NotImplementedError

class GeneralDumper(IDumper):
    """
    For Command Line Testing.
    If running outside Django it overrides the logger.
    Use as:
    dumper = GeneralDumper(request)
    icat = ICat(dumper)
    """
    def __init__(self):
        #
        pass

    def dump_exception(self, exception, message):
        """
        @param exception: Must be a valid python exception
        @param message: Must be a string
        """
        pprint(exception)
        pprint(message)

    def dump_error(self,message):
        """
        @param exception: Must be a valid python exception
        @param message: Must be a string
        """
        pprint(message)

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