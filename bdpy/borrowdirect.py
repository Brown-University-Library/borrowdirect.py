# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import imp, json, logging, pprint, time
import requests
from types import ModuleType, NoneType
from .auth import Authenticator
from .search import Searcher
from .request import Requester


class BorrowDirect( object ):
    """ Manages high-level function calls. """

    def __init__( self, settings=None, logger=None ):
        """
        - Allows a settings module to be passed in,
            or a settings path to be passed in,
            or a dictionary to be passed in. """
        ## general initialization
        self.API_URL_ROOT = None
        self.API_KEY = None
        self.PARTNERSHIP_ID = None
        self.UNIVERSITY_CODE = None
        self.PICKUP_LOCATION = None
        self.LOG_PATH = None
        self.LOG_LEVEL = None
        self.logger = None
        ## setup
        bdh = BorrowDirectHelper()
        normalized_settings = bdh.normalize_settings( settings )
        bdh.update_properties( self, normalized_settings )
        bdh.setup_log( self, logger )
        ## updated by workflow
        self.AId = None
        self.authnz_valid = None
        self.search_result = None
        self.request_result = None

    def run_auth_nz( self, patron_barcode ):
        """ Runs authN/Z and stores authentication-id.
            Can be called manually, but likely no need to, since run_search() and run_request_item() handle auth automatically. """
        self.logger.debug( 'starting run_auth_nz()...' )
        authr = Authenticator( self.logger )
        self.AId = authr.authenticate(
            patron_barcode, self.API_URL_ROOT, self.API_KEY, self.PARTNERSHIP_ID, self.UNIVERSITY_CODE )
        time.sleep( 1 )
        self.authnz_valid = authr.authorize(
            self.API_URL_ROOT, self.AId )
        self.logger.info( 'run_auth_nz() complete' )
        return

    def run_search( self, patron_barcode, search_key, search_value ):
        """ Searches for exact key-value.
            Called manually. """
        self.logger.debug( 'starting run_search()...' )
        srchr = Searcher( self.logger )
        self.search_result = srchr.search( patron_barcode, search_key, search_value, self.API_URL_ROOT, self.API_KEY, self.PARTNERSHIP_ID, self.UNIVERSITY_CODE )
        self.logger.info( 'run_search() complete' )
        return

    def run_request_item( self, patron_barcode, search_key, search_value ):
        """ Requests an exact key-value.
            Called manually. """
        self.logger.debug( 'starting run_request()...' )
        req = Requester( self.logger )
        self.request_result = req.request_item( patron_barcode, search_key, search_value, self.PICKUP_LOCATION, self.API_URL_ROOT, self.API_KEY, self.PARTNERSHIP_ID, self.UNIVERSITY_CODE )
        self.logger.info( 'run_request() complete' )
        return

    # end class BorrowDirect


class BorrowDirectHelper( object ):
    """ Assists BorrowDirect setup.
        Called by BorrowDirect.__init__() """

    def normalize_settings( self, settings ):
        """ Returns a settings module regardless whether settings are passed in as a module or dict or settings-path.
            Called by BorrowDirect.__init__() """
        types = [ NoneType, dict, ModuleType, unicode ]
        assert type(settings) in types, Exception( 'Passing in settings is optional, but if used, must be either a dict, a unicode path to a settings module, or a module named settings; current type is: %s' % repr(type(settings)) )
        if isinstance(settings, dict):
          s = imp.new_module( 'settings' )
          for k, v in settings.items():
            setattr( s, k, v )
          settings = s
        elif isinstance( settings, unicode ):  # path
          settings = imp.load_source( '*', settings )
        return settings

    def update_properties( self, bd_instance, settings ):
        """ Sets main properties.
            Called by BorrowDirect.__init__() """
        bd_instance.API_URL_ROOT = None if ( 'API_URL_ROOT' not in dir(settings) ) else settings.API_URL_ROOT
        bd_instance.API_KEY = None if ( 'API_KEY' not in dir(settings) ) else settings.API_KEY
        bd_instance.PARTNERSHIP_ID = None if ( 'PARTNERSHIP_ID' not in dir(settings) ) else settings.PARTNERSHIP_ID
        bd_instance.UNIVERSITY_CODE = None if ( 'UNIVERSITY_CODE' not in dir(settings) ) else settings.UNIVERSITY_CODE
        bd_instance.PICKUP_LOCATION = None if ( 'PICKUP_LOCATION' not in dir(settings) ) else settings.PICKUP_LOCATION
        bd_instance.LOG_PATH = None if ( 'LOG_PATH' not in dir(settings) ) else settings.LOG_PATH
        bd_instance.LOG_LEVEL = 'DEBUG' if ( 'LOG_LEVEL' not in dir(settings) ) else settings.LOG_LEVEL
        return

    def setup_log( self, bd_instance, logger ):
        """ Configures log path and level.
            Called by BorrowDirect.__init__() """
        if logger:
            bd_instance.logger = logger
        else:
            log_level = {
                'DEBUG': logging.DEBUG, 'INFO': logging.INFO, }
            logging.basicConfig(
                filename=bd_instance.LOG_PATH, level=log_level[bd_instance.LOG_LEVEL],
                format='[%(asctime)s] %(levelname)s [%(module)s-%(funcName)s()::%(lineno)d] %(message)s',
                datefmt='%d/%b/%Y %H:%M:%S' )
            bd_instance.logger = logging.getLogger(__name__)
        return

    # end class BorrowDirectHelper
