# -*- coding: utf-8 -*-

import imp, json, logging, pprint
import requests
from types import ModuleType, NoneType


class BorrowDirect( object ):
    """ Manages high-level function calls. """

    def __init__( self, settings=None ):
        """
        - Allows a settings module to be passed in,
            or a settings path to be passed in,
            or a dictionary to be passed in. """
        ## general initialization
        self.API_AUTH_URL_ROOT = None
        self.UNIVERSITY_CODE = None
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
        self.authnz_is_valid = None

    def say_hi( self ):
        print u'hello_world'

    def run_auth_nz( self, patron_barcode ):
        """ Runs authN/Z and stores authentication-id.
            Called manually. """
        self.logger.debug( u'starting...' )
        self.logger.debug( u'url, `%s`' % self.API_AUTH_URL_ROOT )
        ## authn - get the borrowdirect authentication-id
        d = {
            u'AuthenticationInformation': {
            u'LibrarySymbol': self.UNIVERSITY_CODE,
            u'PatronId': patron_barcode } }
        self.logger.debug( u'params-dict, `%s`' % pprint.pformat(d) )
        headers = { u'Content-type': u'application/json', u'Accept': u'text/plain'}
        r = requests.post( self.API_AUTH_URL_ROOT, data=json.dumps(d), headers=headers )
        self.logger.debug( u'r.content, `%s`' % r.content.decode(u'utf-8') )
        self.logger.debug( u'r.status_code, `%s`' % r.status_code )
        dct = r.json()
        self.logger.debug( u'response dct, `%s`' % pprint.pformat(dct) )
        self.AId = dct[u'Authentication'][u'AuthnUserInfo'][u'AId']
        self.logger.debug( u'self.AId, `%s`' % self.AId )
        return u'foo'

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
        bd_instance.API_AUTH_URL_ROOT = None if ( u'API_AUTH_URL_ROOT' not in dir(settings) ) else settings.API_AUTH_URL_ROOT
        bd_instance.UNIVERSITY_CODE = None if ( u'UNIVERSITY_CODE' not in dir(settings) ) else settings.UNIVERSITY_CODE
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
