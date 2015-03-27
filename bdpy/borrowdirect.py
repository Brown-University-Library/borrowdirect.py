# -*- coding: utf-8 -*-

import imp, json, logging, pprint, time
import requests
from types import ModuleType, NoneType
from .auth import Authenticator
from .search import Searcher


class BorrowDirect( object ):
    """ Manages high-level function calls. """

    def __init__( self, settings=None ):
        """
        - Allows a settings module to be passed in,
            or a settings path to be passed in,
            or a dictionary to be passed in. """
        ## general initialization
        self.API_URL_ROOT = None
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
        bdh.setup_log( self )
        ## updated by workflow
        self.AId = None
        self.authnz_valid = None
        self.search_result = None

    def say_hi( self ):
        print u'hello_world'

    def run_auth_nz( self, patron_barcode ):
        """ Runs authN/Z and stores authentication-id.
            Called manually. """
        self.logger.debug( u'starting run_auth_nz()...' )
        authr = Authenticator( self.logger )
        self.AId = authr.authenticate(
            patron_barcode, self.API_URL_ROOT, self.UNIVERSITY_CODE )
        time.sleep( 1 )
        self.authnz_valid = authr.authorize(
            self.API_URL_ROOT, self.AId )
        self.logger.info( u'run_auth_nz() complete' )
        return

    def run_search( self, patron_barcode, key, value ):
        """ Searches for exact key-value.
            Called manually. """
        self.logger.debug( u'starting run_search...' )
        srchr = Searcher( self.logger )
        self.search_result = srchr.search( patron_barcode, key, value, self.API_URL_ROOT, self.UNIVERSITY_CODE, self.PARTNERSHIP_ID )
        self.logger.info( u'run_search() complete' )
        return

    # end class BorrowDirect


class BorrowDirectHelper( object ):
    """ Assists BorrowDirect setup.
        Called by BorrowDirect.__init__() """

    def normalize_settings( self, settings ):
        """ Returns a settings module regardless whether settings are passed in as a module or dict or settings-path.
            Called by BorrowDirect.__init__() """
        types = [ NoneType, dict, ModuleType, unicode ]
        assert type(settings) in types, Exception( u'Passing in settings is optional, but if used, must be either a dict, a unicode path to a settings module, or a module named settings; current type is: %s' % repr(type(settings)) )
        if isinstance(settings, dict):
          s = imp.new_module( u'settings' )
          for k, v in settings.items():
            setattr( s, k, v )
          settings = s
        elif isinstance( settings, unicode ):  # path
          settings = imp.load_source( u'*', settings )
        return settings

    def update_properties( self, bd_instance, settings ):
        """ Sets main properties.
            Called by BorrowDirect.__init__() """
        bd_instance.API_URL_ROOT = None if ( u'API_URL_ROOT' not in dir(settings) ) else settings.API_URL_ROOT
        bd_instance.PARTNERSHIP_ID = None if ( u'PARTNERSHIP_ID' not in dir(settings) ) else settings.PARTNERSHIP_ID
        bd_instance.UNIVERSITY_CODE = None if ( u'UNIVERSITY_CODE' not in dir(settings) ) else settings.UNIVERSITY_CODE
        bd_instance.PICKUP_LOCATION = None if ( u'PICKUP_LOCATION' not in dir(settings) ) else settings.PICKUP_LOCATION
        bd_instance.LOG_PATH = None if ( u'LOG_PATH' not in dir(settings) ) else settings.LOG_PATH
        bd_instance.LOG_LEVEL = u'DEBUG' if ( u'LOG_LEVEL' not in dir(settings) ) else settings.LOG_LEVEL
        return

    def setup_log( self, bd_instance ):
        """ Configures log path and level.
            Called by BorrowDirect.__init__() """
        log_level = {
            u'DEBUG': logging.DEBUG,
            u'INFO': logging.INFO, }
        logging.basicConfig(
            filename=bd_instance.LOG_PATH, level=log_level[bd_instance.LOG_LEVEL],
            format='dt %(asctime)s | ln %(lineno)d | md %(module)s | fn %(funcName)s | %(message)s' )
        bd_instance.logger = logging.getLogger(__name__)
        return

    # end class BorrowDirectHelper
