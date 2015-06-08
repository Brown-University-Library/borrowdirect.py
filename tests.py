# -*- coding: utf-8 -*-

import exceptions, imp, pprint, os, time, unittest
from bdpy import BorrowDirect
from bdpy.auth import Authenticator
from bdpy.search import Searcher
from bdpy.request import Requester


SLEEP_SECONDS = 2  # test-server is creaky


class BorrowDirectTests( unittest.TestCase ):

    def setUp(self):
        self.LOG_PATH = unicode( os.environ[u'BDPY_TEST__LOG_PATH'] )  # if None  ...outputs to console
        time.sleep( SLEEP_SECONDS )
        self.patron_barcode = unicode( os.environ[u'BDPY_TEST__PATRON_BARCODE'] )
        self.api_url_root = unicode( os.environ[u'BDPY_TEST__API_URL_ROOT'] )
        self.university_code = unicode( os.environ[u'BDPY_TEST__UNIVERSITY_CODE'] )
        self.partnership_id = unicode( os.environ[u'BDPY_TEST__PARTNERSHIP_ID'] )
        self.pickup_location = unicode(os.environ[u'BDPY_TEST__PICKUP_LOCATION'])

    def test_settings_instantiation(self):
        """ Tests that instance instantiation handles settings not-defined, or defined as dict, module, or path. """
        ## no settings passed on instantiation
        bd = BorrowDirect()  # no settings info
        self.assertEqual(
            True, isinstance(bd, BorrowDirect) )
        ## dict settings
        settings_dict = {}  ## empty dct
        bd = BorrowDirect( settings_dict )
        self.assertEqual(
            None, bd.UNIVERSITY_CODE )
        settings_dict = { u'UNIVERSITY_CODE': u'123' }  ## populated dct
        bd = BorrowDirect( settings_dict )
        self.assertEqual(
            u'123', bd.UNIVERSITY_CODE )
        ## module settings
        s = imp.new_module( u'settings' )  ## empty module
        bd = BorrowDirect( s )
        self.assertEqual(
            None, bd.UNIVERSITY_CODE )
        s = imp.new_module( u'settings' )  ## populated module
        s.UNIVERSITY_CODE = u'234'
        bd = BorrowDirect( s )
        self.assertEqual(
            u'234', bd.UNIVERSITY_CODE )

    def test_run_auth_nz(self):
        """ Tests manager authN/Z. """
        basics = {
            u'UNIVERSITY_CODE': self.university_code, u'API_URL_ROOT': self.api_url_root, u'LOG_PATH': self.LOG_PATH }
        bd = BorrowDirect( basics )
        bd.run_auth_nz( self.patron_barcode )
        self.assertEqual(
            True, bd.authnz_valid )

    def test_run_search(self):
        """ Tests manager item availability check. """
        basics = {
            u'UNIVERSITY_CODE': self.university_code, u'API_URL_ROOT': self.api_url_root, u'PARTNERSHIP_ID': self.partnership_id, u'LOG_PATH': self.LOG_PATH }
        bd = BorrowDirect( basics )
        search_value = unicode(os.environ[u'BDPY_TEST__ISBN_BROWN_NO_AND_BD_REQUESTABLE'])
        bd.run_search( self.patron_barcode, u'ISBN', search_value )
        for key in [u'AuthorizationId', u'Available', u'PickupLocations', u'SearchTerm']:
            self.assertTrue(
                key in bd.search_result[u'Item'].keys() )
        # NOTE: where is the 'RequestLink' key?

    def test_run_request_item(self):
        """ Tests manager requesting. """
        basics = {
            u'UNIVERSITY_CODE': self.university_code, u'API_URL_ROOT': self.api_url_root, u'PARTNERSHIP_ID': self.partnership_id, u'PICKUP_LOCATION': self.pickup_location, u'LOG_PATH': self.LOG_PATH }
        bd = BorrowDirect( basics )
        search_value = unicode(os.environ[u'BDPY_TEST__ISBN_BROWN_NO_AND_BD_REQUESTABLE'])
        bd.run_request_item( self.patron_barcode, u'ISBN', search_value )
        self.assertEqual(
            [u'Request'], bd.request_result.keys() )
        self.assertEqual(
            [u'RequestNumber'], bd.request_result[u'Request'].keys() )
        self.assertEqual(
            u'BRO-', bd.request_result[u'Request'][u'RequestNumber'][0:4] )

    # end class BorrowDirectTests


class AuthenticatorTests( unittest.TestCase ):

    def setUp(self):
        time.sleep( SLEEP_SECONDS )
        self.LOG_PATH = unicode( os.environ[u'BDPY_TEST__LOG_PATH'] )  # if None  ...outputs to console
        bd = BorrowDirect( {u'LOG_PATH': self.LOG_PATH} )
        self.logger = bd.logger
        self.patron_barcode = unicode(os.environ[u'BDPY_TEST__PATRON_BARCODE'])
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
        self.patron_barcode = unicode(os.environ[u'BDPY_TEST__PATRON_BARCODE'])
        self.api_url_root = unicode(os.environ[u'BDPY_TEST__API_URL_ROOT'])
        self.university_code = unicode(os.environ[u'BDPY_TEST__UNIVERSITY_CODE'])
        self.partnership_id = unicode(os.environ[u'BDPY_TEST__PARTNERSHIP_ID'])

    def test_search(self):
        """ Tests basic key-value search. """
        s = Searcher( self.logger )
        ( search_key, search_value ) = ( u'ISBN', u'9780688002305' )  # Zen & the Art of Motorcycle Maintenance (also #0688002307)
        result_dct = s.search(
            self.patron_barcode, search_key, search_value, self.api_url_root, self.university_code, self.partnership_id )
        for key in [u'AuthorizationId', u'Available', u'PickupLocations', u'SearchTerm']:
            self.assertTrue(
                key in result_dct[u'Item'].keys() )
        # NOTE: where is the 'RequestLink' key?

    # end class SearcherTests


class RequesterTests( unittest.TestCase ):

    def setUp(self):
        time.sleep( SLEEP_SECONDS )
        self.LOG_PATH = unicode( os.environ[u'BDPY_TEST__LOG_PATH'] )  # if None  ...outputs to console
        bd = BorrowDirect( {u'LOG_PATH': self.LOG_PATH} )
        self.logger = bd.logger
        self.patron_barcode = unicode(os.environ[u'BDPY_TEST__PATRON_BARCODE'])
        self.api_url_root = unicode(os.environ[u'BDPY_TEST__API_URL_ROOT'])
        self.university_code = unicode(os.environ[u'BDPY_TEST__UNIVERSITY_CODE'])
        self.partnership_id = unicode(os.environ[u'BDPY_TEST__PARTNERSHIP_ID'])
        self.pickup_location = unicode(os.environ[u'BDPY_TEST__PICKUP_LOCATION'])

    def test_request_item__brown_no_and_bd_yes(self):
        """ Tests exact key-value requesting when...
                - item not held by Brown
                - item requestable in BorrowDirect web-interface """
        r = Requester( self.logger )
        search_key = u'ISBN'
        search_value = unicode(os.environ[u'BDPY_TEST__ISBN_BROWN_NO_AND_BD_REQUESTABLE'])
        request_result_dct = r.request_item( search_key, search_value, self.pickup_location, self.api_url_root, self.patron_barcode, self.university_code, self.partnership_id )
        self.assertEqual(
            [u'Request'], request_result_dct.keys() )
        self.assertEqual(
            [u'RequestNumber'], request_result_dct[u'Request'].keys() )
        self.assertEqual(
            u'BRO-', request_result_dct[u'Request'][u'RequestNumber'][0:4] )

    def test_build_params( self ):
        """ Tests for all expected params. """
        r = Requester( self.logger )
        ( partnership_id, authorization_id, pickup_location, search_key, search_value ) = ( u'a', u'b', u'c', u'd', u'e' )
        params = r.build_params( partnership_id, authorization_id, pickup_location, search_key, search_value )
        self.assertEqual( [u'AuthorizationId', u'ExactSearch', u'Notes', u'PartnershipId', u'PickupLocation'], sorted(params.keys()) )




if __name__ == "__main__":
  unittest.main()
