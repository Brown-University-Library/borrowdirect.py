# -*- coding: utf-8 -*-

from types import ModuleType, NoneType


class BorrowDirect( object ):
    """ Manages high-level function calls. """

    def __init__( self, settings=None ):
        """
        - Allows a settings module to be passed in,
            or a settings path to be passed in,
            or a dictionary to be passed in.
        - Sets other attributes.
        - Attributes in caps are passed in; others are calculated.
        """
        types = [ NoneType, dict, ModuleType, unicode ]
        assert type(settings) in types, Exception( u'Passing in settings is optional, but if used, must be either a dict, a unicode path to a settings module, or a module named settings; current type is: %s' % repr(type(settings)) )
        if isinstance(settings, dict):
          s = imp.new_module( u'settings' )
          for k, v in settings.items():
            setattr( s, k, v )
          settings = s
        elif isinstance(settings, ModuleType):
          pass
        elif isinstance(settings, unicode):  # path
          settings = imp.load_source( u'*', settings )
        ## general
        self.BD_API_URL = None if ( u'BD_API_URL' not in dir(settings) ) else settings.BD_API_URL
        self.UNIVERSITY_CODE = None if ( u'UNIVERSITY_CODE' not in dir(settings) ) else settings.UNIVERSITY_CODE
        self.LOG_PATH = None if ( u'LOG_PATH' not in dir(settings) ) else settings.LOG_PATH

    def say_hi( self ):
        print u'BD_API_URL, %s' % self.BD_API_URL
        print u'UNIVERSITY_CODE, %s' % self.UNIVERSITY_CODE
        print u'LOG_PATH, %s' % self.LOG_PATH
