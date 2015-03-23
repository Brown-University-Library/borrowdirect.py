# -*- coding: utf-8 -*-

import imp, pprint
import requests
from types import ModuleType, NoneType


class BorrowDirect( object ):
    """ Manages high-level function calls. """

    def __init__( self, settings=None ):
        """
        - Allows a settings module to be passed in,
            or a settings path to be passed in,
            or a dictionary to be passed in. """
        ## general
        self.API_AUTH_URL_ROOT = None
        self.UNIVERSITY_CODE = None
        self.LOG_PATH = None
        normalized_settings = self.normalize_settings( settings )
        self.update_properties( normalized_settings )
        self.authentication_id = None
        self.authnz_is_valid = False

    def normalize_settings( self, settings ):
        """ Returns a settings module regardless of module or dict or settings-path.
            Called by __init__() """
        types = [ NoneType, dict, ModuleType, unicode ]
        assert type(settings) in types, Exception( u'Passing in settings is optional, but if used, must be either a dict, a unicode path to a settings module, or a module named settings; current type is: %s' % repr(type(settings)) )
        if isinstance(settings, dict):
          s = imp.new_module( u'settings' )
          for k, v in settings.items():
            setattr( s, k, v )
          settings = s
        elif isinstance(settings, unicode):  # path
          settings = imp.load_source( u'*', settings )
        return settings

    def update_properties( self, settings ):
        """ Sets main properties.
            Called by __init__() """
        self.API_AUTH_URL_ROOT = None if ( u'API_AUTH_URL_ROOT' not in dir(settings) ) else settings.API_AUTH_URL_ROOT
        self.UNIVERSITY_CODE = None if ( u'UNIVERSITY_CODE' not in dir(settings) ) else settings.UNIVERSITY_CODE
        self.LOG_PATH = None if ( u'LOG_PATH' not in dir(settings) ) else settings.LOG_PATH
        return

    def say_hi( self ):
        print u'API_AUTH_URL_ROOT, %s' % self.API_AUTH_URL_ROOT
        print u'UNIVERSITY_CODE, %s' % self.UNIVERSITY_CODE
        print u'LOG_PATH, %s' % self.LOG_PATH

    def run_auth_nz( self, patron_barcode ):
        """ Runs authN/Z and stores authentication-id.
            Called manually. """
        ## authn
        d = { u'AuthenticationInformation': {
                u'LibrarySymbol': self.UNIVERSITY_CODE,
                u'PatronId': patron_barcode } }
        headers = { u'Content-type': u'application/json', u'Accept': u'text/plain'}
        r = requests.post( self.API_AUTH_URL_ROOT, data=json.dumps(d), headers=headers )
        pprint.pprint( r.content )
        return u'foo'
