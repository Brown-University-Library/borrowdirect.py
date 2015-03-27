# -*- coding: utf-8 -*-

import exceptions, imp, pprint, os, time, unittest
from bdpy import BorrowDirect
from bdpy.auth import Authenticator
from bdpy.search import Searcher


SLEEP_SECONDS = 2  # test-server is creaky


class BorrowDirectTests( unittest.TestCase ):

    def setUp(self):
        self.LOG_PATH = unicode( os.environ[u'BDPY_TEST__LOG_PATH'] )  # if None  ...outputs to console
        time.sleep( SLEEP_SECONDS )

    def test_settings_instantiation(self):
        """ Tests that module instantiation handles settings not-defined, or defined as dict, module, or path. """
        ## no settings passed on instantiation
        bd = BorrowDirect()  # no settings info
        self.assertEqual(
            True, isinstance(bd, BorrowDirect) )
        ## dict settings
        settings_dict = {}  ## test empty
        bd = BorrowDirect( settings_dict )
        self.assertEqual(
            None, bd.UNIVERSITY_CODE )
        settings_dict = { u'UNIVERSITY_CODE': u'123' }  ## test populated
        bd = BorrowDirect( settings_dict )
        self.assertEqual(
            u'123', bd.UNIVERSITY_CODE )
        ## module settings
        s = imp.new_module( u'settings' )  ## test empty
        bd = BorrowDirect( s )
        self.assertEqual(
            None, bd.UNIVERSITY_CODE )
        s = imp.new_module( u'settings' )  ## test populated
        s.UNIVERSITY_CODE = u'234'
        bd = BorrowDirect( s )
        self.assertEqual(
            u'234', bd.UNIVERSITY_CODE )

    def test_run_auth_nz(self):
        """ Tests successful and unsucessful authN/Z. """
        ## good patron
        data = {
            u'UNIVERSITY_CODE': unicode( os.environ[u'BDPY_TEST__UNIVERSITY_CODE'] ),
            u'API_URL_ROOT': unicode( os.environ[u'BDPY_TEST__API_URL_ROOT'] ),
            u'LOG_PATH': self.LOG_PATH }
        bd = BorrowDirect( data )
        bd.run_auth_nz( unicode(os.environ[u'BDPY_TEST__PATRON_BARCODE_GOOD']) )
        self.assertEqual(
            True, bd.authnz_valid )

    def test_run_search(self):
        """ Tests item availability. """
        data = {
            u'UNIVERSITY_CODE': unicode( os.environ[u'BDPY_TEST__UNIVERSITY_CODE'] ),
            u'API_URL_ROOT': unicode( os.environ[u'BDPY_TEST__API_URL_ROOT'] ),
            u'API_PARTNERSHIP_ID': unicode( os.environ[u'BDPY_TEST__PARTNERSHIP_ID'] ),
            u'LOG_PATH': self.LOG_PATH }
        bd = BorrowDirect( data )
        patron_barcode = unicode(os.environ[u'BDPY_TEST__PATRON_BARCODE_GOOD'])
        result_dct = bd.search( patron_barcode, u'ISBN', u'9780688002305' )  # Zen & the Art of Motorcycle Maintenance (also #0688002307)
        # bd.search( patron_barcode, u'ISBN', u'9780307269706' )
        # bd.search( patron_barcode, u'ISBN', u'0745649890' )
        for key in [u'AuthorizationId', u'Available', u'PickupLocations', u'SearchTerm']:
            self.assertTrue(
                key in result_dct[u'Item'].keys() )
        # NOTE: where is the 'RequestLink' key?

    # def test_search(self):
    #     """ Tests item availability. """
    #     data = {
    #         u'UNIVERSITY_CODE': unicode( os.environ[u'BDPY_TEST__UNIVERSITY_CODE'] ),
    #         u'API_URL_ROOT': unicode( os.environ[u'BDPY_TEST__API_URL_ROOT'] ),
    #         u'API_PARTNERSHIP_ID': unicode( os.environ[u'BDPY_TEST__PARTNERSHIP_ID'] ),
    #         u'LOG_PATH': self.LOG_PATH }
    #     bd = BorrowDirect( data )
    #     patron_barcode = unicode(os.environ[u'BDPY_TEST__PATRON_BARCODE_GOOD'])
    #     result_dct = bd.search( patron_barcode, u'ISBN', u'9780688002305' )  # Zen & the Art of Motorcycle Maintenance (also #0688002307)
    #     # bd.search( patron_barcode, u'ISBN', u'9780307269706' )
    #     # bd.search( patron_barcode, u'ISBN', u'0745649890' )
    #     for key in [u'AuthorizationId', u'Available', u'PickupLocations', u'SearchTerm']:
    #         self.assertTrue(
    #             key in result_dct[u'Item'].keys() )
    #     # NOTE: where is the 'RequestLink' key?

    # end class BorrowDirectTests


class AuthenticatorTests( unittest.TestCase ):

    def setUp(self):
        time.sleep( SLEEP_SECONDS )
        self.LOG_PATH = unicode( os.environ[u'BDPY_TEST__LOG_PATH'] )  # if None  ...outputs to console
        bd = BorrowDirect( {u'LOG_PATH': self.LOG_PATH} )
        self.logger = bd.logger
        self.patron_barcode = unicode(os.environ[u'BDPY_TEST__PATRON_BARCODE_GOOD'])
        self.api_url_root = unicode(os.environ[u'BDPY_TEST__API_URL_ROOT'])
        self.university_code = unicode(os.environ[u'BDPY_TEST__UNIVERSITY_CODE'])

    def test_authenticate(self):
        """ Tests getting an authentication-id. """
        a = Authenticator( self.logger )
        authentication_id = a.authenticate(
            self.patron_barcode, self.api_url_root, self.university_code )
        self.assertEqual(
            27, len(authentication_id) )

    def test_authorize(self):
        """ Tests authz session-extender. """
        a = Authenticator( self.logger )
        authentication_id = a.authenticate(
            self.patron_barcode, self.api_url_root, self.university_code )
        time.sleep( SLEEP_SECONDS )
        validity = a.authorize(
            self.api_url_root, authentication_id )
        self.assertEqual(
            True, validity )

    # end class AuthTests


class SearcherTests( unittest.TestCase ):

    def setUp(self):
        time.sleep( SLEEP_SECONDS )
        self.LOG_PATH = unicode( os.environ[u'BDPY_TEST__LOG_PATH'] )  # if None  ...outputs to console
        bd = BorrowDirect( {u'LOG_PATH': self.LOG_PATH} )
        self.logger = bd.logger
        self.patron_barcode = unicode(os.environ[u'BDPY_TEST__PATRON_BARCODE_GOOD'])
        self.api_url_root = unicode(os.environ[u'BDPY_TEST__API_URL_ROOT'])
        self.university_code = unicode(os.environ[u'BDPY_TEST__UNIVERSITY_CODE'])
        self.api_partnership_id = unicode(os.environ[u'BDPY_TEST__PARTNERSHIP_ID'])

    def test_search(self):
        """ Tests basic key-value search. """
        s = Searcher( self.logger )
        ( search_key, search_value ) = ( u'ISBN', u'9780688002305' )  # Zen & the Art of Motorcycle Maintenance (also #0688002307)
        result_dct = s.search(
            self.patron_barcode, search_key, search_value, self.api_url_root, self.university_code, self.api_partnership_id )
        for key in [u'AuthorizationId', u'Available', u'PickupLocations', u'SearchTerm']:
            self.assertTrue(
                key in result_dct[u'Item'].keys() )
        # NOTE: where is the 'RequestLink' key?

    # end class SearcherTests




if __name__ == "__main__":
  unittest.main()
