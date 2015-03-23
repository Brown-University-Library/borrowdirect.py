# -*- coding: utf-8 -*-

import imp
from types import ModuleType, NoneType


class BorrowDirect( object ):
    """ Manages high-level function calls. """

    def __init__( self, settings=None ):
        """
        - Allows a settings module to be passed in,
            or a settings path to be passed in,
            or a dictionary to be passed in. """
        ## general
        self.BD_API_URL = None
        self.UNIVERSITY_CODE = None
        self.LOG_PATH = None
        normalized_settings = self.normalize_settings( settings )
        self.update_properties( normalized_settings )

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
        self.BD_API_URL = None if ( u'BD_API_URL' not in dir(settings) ) else settings.BD_API_URL
        self.UNIVERSITY_CODE = None if ( u'UNIVERSITY_CODE' not in dir(settings) ) else settings.UNIVERSITY_CODE
        self.LOG_PATH = None if ( u'LOG_PATH' not in dir(settings) ) else settings.LOG_PATH
        return

    def say_hi( self ):
        print u'BD_API_URL, %s' % self.BD_API_URL
        print u'UNIVERSITY_CODE, %s' % self.UNIVERSITY_CODE
        print u'LOG_PATH, %s' % self.LOG_PATH
