# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import exceptions, imp, pprint, os, time, unittest
from bdpy import BorrowDirect
from bdpy.auth import Authenticator
from bdpy.search import Searcher
from bdpy.request import Requester


SLEEP_SECONDS = 2  # being nice


class BorrowDirectTests( unittest.TestCase ):

    def setUp(self):
        self.LOG_PATH = unicode( os.environ['BDPY_TEST__LOG_PATH'] )  # if None  ...outputs to console
        time.sleep( SLEEP_SECONDS )
        self.patron_barcode = unicode( os.environ['BDPY_TEST__PATRON_BARCODE'] )
        self.api_url_root = unicode( os.environ['BDPY_TEST__API_URL_ROOT'] )
        self.university_code = unicode( os.environ['BDPY_TEST__UNIVERSITY_CODE'] )
        self.partnership_id = unicode( os.environ['BDPY_TEST__PARTNERSHIP_ID'] )
        self.pickup_location = unicode(os.environ['BDPY_TEST__PICKUP_LOCATION'])

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
        settings_dict = { 'UNIVERSITY_CODE': '123' }  ## populated dct
        bd = BorrowDirect( settings_dict )
        self.assertEqual(
            '123', bd.UNIVERSITY_CODE )
        ## module settings
        s = imp.new_module( 'settings' )  ## empty module
        bd = BorrowDirect( s )
        self.assertEqual(
            None, bd.UNIVERSITY_CODE )
        s = imp.new_module( 'settings' )  ## populated module
        s.UNIVERSITY_CODE = '234'
        bd = BorrowDirect( s )
        self.assertEqual(
            '234', bd.UNIVERSITY_CODE )

    def test_run_auth_nz(self):
        """ Tests manager authN/Z. """
        basics = {
            'UNIVERSITY_CODE': self.university_code, 'API_URL_ROOT': self.api_url_root, 'LOG_PATH': self.LOG_PATH }
        bd = BorrowDirect( basics )
        bd.run_auth_nz( self.patron_barcode )
        self.assertEqual(
            True, bd.authnz_valid )

    def test_run_search(self):
        """ Tests manager item availability check. """
        basics = {
            'UNIVERSITY_CODE': self.university_code, 'API_URL_ROOT': self.api_url_root, 'PARTNERSHIP_ID': self.partnership_id, 'LOG_PATH': self.LOG_PATH }
        bd = BorrowDirect( basics )
        search_value = unicode(os.environ['BDPY_TEST__ISBN_BROWN_NO_AND_BD_REQUESTABLE'])
        bd.run_search( self.patron_barcode, 'ISBN', search_value )
        for key in ['AuthorizationId', 'Available', 'PickupLocations', 'SearchTerm']:
            self.assertTrue(
                key in bd.search_result['Item'].keys() )
        # NOTE: where is the 'RequestLink' key?

    # def test_run_request_item(self):
    #     """ Tests manager requesting.
    #         Commented out because it'll really request the item. """
    #     basics = {
    #         'UNIVERSITY_CODE': self.university_code, 'API_URL_ROOT': self.api_url_root, 'PARTNERSHIP_ID': self.partnership_id, 'PICKUP_LOCATION': self.pickup_location, 'LOG_PATH': self.LOG_PATH }
    #     bd = BorrowDirect( basics )
    #     search_value = unicode(os.environ['BDPY_TEST__ISBN_BROWN_NO_AND_BD_REQUESTABLE'])
    #     bd.run_request_item( self.patron_barcode, 'ISBN', search_value )
    #     self.assertEqual(
    #         ['Request'], bd.request_result.keys() )
    #     self.assertEqual(
    #         ['RequestNumber'], bd.request_result['Request'].keys() )
    #     self.assertEqual(
    #         'BRO-', bd.request_result['Request']['RequestNumber'][0:4] )

    # end class BorrowDirectTests


class AuthenticatorTests( unittest.TestCase ):

    def setUp(self):
        time.sleep( SLEEP_SECONDS )
        self.LOG_PATH = unicode( os.environ['BDPY_TEST__LOG_PATH'] )  # if None  ...outputs to console
        bd = BorrowDirect( {'LOG_PATH': self.LOG_PATH} )
        self.logger = bd.logger
        self.patron_barcode = unicode( os.environ['BDPY_TEST__PATRON_BARCODE'] )
        self.api_url_root = unicode( os.environ['BDPY_TEST__API_URL_ROOT'] )
        self.api_key = unicode( os.environ['BDPY_TEST__API_KEY'] )
        self.university_code = unicode( os.environ['BDPY_TEST__UNIVERSITY_CODE'] )
        self.partnership_id = unicode( os.environ['BDPY_TEST__PARTNERSHIP_ID'] )

    def test_authenticate(self):
        """ Tests getting an authentication-id. """
        a = Authenticator( self.logger )
        authentication_id = a.authenticate(
            self.patron_barcode, self.api_url_root, self.api_key, self.university_code, self.partnership_id )
        self.assertEqual(
            27, len(authentication_id) )

    def test_authorize(self):
        """ Tests authz session-extender. """
        a = Authenticator( self.logger )
        authentication_id = a.authenticate(
            self.patron_barcode, self.api_url_root, self.api_key, self.university_code, self.partnership_id )
        time.sleep( SLEEP_SECONDS )
        validity = a.authorize(
            self.api_url_root, authentication_id )
        self.assertEqual(
            True, validity )

    # end class AuthenticatorTests


class SearcherTests( unittest.TestCase ):

    def setUp(self):
        time.sleep( SLEEP_SECONDS )
        self.LOG_PATH = unicode( os.environ['BDPY_TEST__LOG_PATH'] )  # if None  ...outputs to console
        bd = BorrowDirect( {'LOG_PATH': self.LOG_PATH} )
        self.logger = bd.logger
        self.patron_barcode = unicode( os.environ['BDPY_TEST__PATRON_BARCODE'] )
        self.api_url_root = unicode( os.environ['BDPY_TEST__API_URL_ROOT'] )
        self.api_key = unicode( os.environ['BDPY_TEST__API_KEY'] )
        self.university_code = unicode( os.environ['BDPY_TEST__UNIVERSITY_CODE'] )
        self.partnership_id = unicode( os.environ['BDPY_TEST__PARTNERSHIP_ID'] )
        self.isbn_unavailable = unicode( os.environ['BDPY_TEST__ISBN_UNAVAILABLE'] )
        self.isb_available = unicode( os.environ['BDPY_TEST__ISBN_AVAILABLE'] )

    def test_search_unavailable(self):
        """ Tests basic isbn search for unavailable item. """
        s = Searcher( self.logger )
        ( search_key, search_value ) = ( 'ISBN', self.isbn_unavailable )
        result_dct = s.search(
            self.patron_barcode, search_key, search_value, self.api_url_root, self.api_key, self.university_code, self.partnership_id )
        self.assertEqual(
            ['Available', 'RequestLink', 'SearchTerm'], sorted(result_dct.keys()) )
        self.assertEqual(
            False, result_dct['Available'] )

    def test_search_available(self):
        """ Tests basic isbn search for available item. """
        s = Searcher( self.logger )
        ( search_key, search_value ) = ( 'ISBN', self.isb_available )
        result_dct = s.search(
            self.patron_barcode, search_key, search_value, self.api_url_root, self.api_key, self.university_code, self.partnership_id )
        self.assertEqual(
            ['Available', 'PickupLocation', 'RequestLink', 'SearchTerm'], sorted(result_dct.keys()) )
        self.assertEqual(
            True, result_dct['Available'] )

    # end class SearcherTests


class RequesterTests( unittest.TestCase ):

    def setUp(self):
        time.sleep( SLEEP_SECONDS )
        self.LOG_PATH = unicode( os.environ['BDPY_TEST__LOG_PATH'] )  # if None  ...outputs to console
        bd = BorrowDirect( {'LOG_PATH': self.LOG_PATH} )
        self.logger = bd.logger
        self.patron_barcode = unicode( os.environ['BDPY_TEST__PATRON_BARCODE'] )
        self.api_url_root = unicode( os.environ['BDPY_TEST__API_URL_ROOT'] )
        self.api_key = unicode( os.environ['BDPY_TEST__API_KEY'] )
        self.university_code = unicode( os.environ['BDPY_TEST__UNIVERSITY_CODE'] )
        self.partnership_id = unicode( os.environ['BDPY_TEST__PARTNERSHIP_ID'] )
        self.pickup_location = unicode( os.environ['BDPY_TEST__PICKUP_LOCATION'] )
        self.isbn_unavailable = unicode( os.environ['BDPY_TEST__ISBN_UNAVAILABLE'] )
        self.isbn_available = unicode( os.environ['BDPY_TEST__ISBN_AVAILABLE'] )

    ## uncomment the two tests to really attempt requests

    # def test_request_item_unavailable(self):
    #     """ Tests basic isbn request for unavailable item.
    #         NOTE: will really attempt a request. """
    #     r = Requester( self.logger )
    #     ( search_key, search_value ) = ( 'ISBN', self.isbn_unavailable )
    #     result_dct = r.request_item(
    #         self.patron_barcode, search_key, search_value, self.pickup_location, self.api_url_root, self.api_key, self.university_code, self.partnership_id )
    #     self.assertEqual(
    #         ['RequestLink'], sorted(result_dct.keys()) )
    #     self.assertEqual(
    #         ['ButtonLabel', 'ButtonLink', 'RequestMessage'], sorted(result_dct['RequestLink'].keys()) )

    # def test_request_item_available(self):
    #     """ Tests basic isbn request for available item.
    #         NOTE: will really attempt a request. """
    #     r = Requester( self.logger )
    #     ( search_key, search_value ) = ( 'ISBN', self.isbn_available )
    #     result_dct = r.request_item(
    #         self.patron_barcode, search_key, search_value, self.pickup_location, self.api_url_root, self.api_key, self.university_code, self.partnership_id )
    #     self.assertEqual(
    #         ['RequestNumber'], sorted(result_dct.keys()) )
    #     self.assertEqual(
    #         'BRO-', request_result_dct['RequestNumber'][0:4] )

    def test_build_params( self ):
        """ Tests for all expected params. """
        r = Requester( self.logger )
        ( partnership_id, authorization_id, pickup_location, search_key, search_value ) = ( 'a', 'b', 'c', 'd', 'e' )
        params = r.build_params( partnership_id, authorization_id, pickup_location, search_key, search_value )
        self.assertEqual(
            ['ExactSearch', 'Notes', 'PartnershipId', 'PickupLocation'],
            sorted(params.keys()) )

    # end class RequesterTests


if __name__ == '__main__':
  unittest.main()
