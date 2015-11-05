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
        self.api_key = unicode( os.environ['BDPY_TEST__API_KEY'] )
        self.university_code = unicode( os.environ['BDPY_TEST__UNIVERSITY_CODE'] )
        self.partnership_id = unicode( os.environ['BDPY_TEST__PARTNERSHIP_ID'] )
        self.pickup_location = unicode( os.environ['BDPY_TEST__PICKUP_LOCATION'] )
        self.isbn_found_and_available = unicode( os.environ['BDPY_TEST__ISBN_FOUND_AND_AVAILABLE'] )
        self.isbn_found_and_unavailable = unicode( os.environ['BDPY_TEST__ISBN_FOUND_AND_UNAVAILABLE'] )
        self.isbn_not_found = unicode( os.environ['BDPY_TEST__ISBN_NOT_FOUND'] )

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
            'API_URL_ROOT': self.api_url_root,
            'API_KEY': self.api_key,
            'PARTNERSHIP_ID': self.partnership_id,
            'UNIVERSITY_CODE': self.university_code,
            'LOG_PATH': self.LOG_PATH }
        bd = BorrowDirect( basics )
        bd.run_auth_nz( self.patron_barcode )
        self.assertEqual(
            True, bd.authnz_valid )

    def test_run_search__found_and_available(self):
        """ Tests search for item found and available. """
        basics = {
            'API_URL_ROOT': self.api_url_root,
            'API_KEY': self.api_key,
            'PARTNERSHIP_ID': self.partnership_id,
            'UNIVERSITY_CODE': self.university_code,
            'LOG_PATH': self.LOG_PATH }
        bd = BorrowDirect( basics )
        bd.run_search( self.patron_barcode, 'ISBN', self.isbn_found_and_available )
        # print bd.search_result
        self.assertEqual( ['Available', 'PickupLocation', 'RequestLink', 'SearchTerm'], sorted(bd.search_result.keys()) )
        self.assertEqual( True, bd.search_result['Available'] )

    def test_run_search__found_and_unavailable(self):
        """ Tests search for item found and unavailable. """
        basics = {
            'API_URL_ROOT': self.api_url_root,
            'API_KEY': self.api_key,
            'PARTNERSHIP_ID': self.partnership_id,
            'UNIVERSITY_CODE': self.university_code,
            'LOG_PATH': self.LOG_PATH }
        bd = BorrowDirect( basics )
        bd.run_search( self.patron_barcode, 'ISBN', self.isbn_found_and_unavailable )
        self.assertEqual( ['Available', 'RequestLink', 'SearchTerm'], sorted(bd.search_result.keys()) )
        self.assertEqual( False, bd.search_result['Available'] )

    def test_run_search__not_found(self):
        """ Tests search for item not found. """
        basics = {
            'API_URL_ROOT': self.api_url_root,
            'API_KEY': self.api_key,
            'PARTNERSHIP_ID': self.partnership_id,
            'UNIVERSITY_CODE': self.university_code,
            'LOG_PATH': self.LOG_PATH }
        bd = BorrowDirect( basics )
        bd.run_search( self.patron_barcode, 'ISBN', self.isbn_not_found )
        self.assertEqual(
            {"Problem":{"ErrorCode":"PUBFI002","ErrorMessage":"No result"}}, bd.search_result )

    # def test_run_request_item__found_and_available(self):
    #     """ Tests manager requesting.
    #         Commented out because it'll really request the item. """
    #     basics = {
    #         'API_URL_ROOT': self.api_url_root,
    #         'API_KEY': self.api_key,
    #         'PARTNERSHIP_ID': self.partnership_id,
    #         'UNIVERSITY_CODE': self.university_code,
    #         'PICKUP_LOCATION': self.pickup_location,
    #         'LOG_PATH': self.LOG_PATH }
    #     bd = BorrowDirect( basics )
    #     bd.run_request_item( self.patron_barcode, 'ISBN', self.isbn_found_and_available )
    #     self.assertEqual(
    #         ['RequestNumber'], sorted(bd.request_result.keys()) )
    #     self.assertEqual(
    #         'BRO-', bd.request_result['RequestNumber'][0:4] )

    def test_run_request_item__not_found(self):
        """ Tests manager requesting on not-found item.
            Note that this will really attempt the request. """
        basics = {
            'API_URL_ROOT': self.api_url_root,
            'API_KEY': self.api_key,
            'PARTNERSHIP_ID': self.partnership_id,
            'UNIVERSITY_CODE': self.university_code,
            'PICKUP_LOCATION': self.pickup_location,
            'LOG_PATH': self.LOG_PATH }
        bd = BorrowDirect( basics )
        bd.run_request_item( self.patron_barcode, 'ISBN', self.isbn_not_found )
        self.assertEqual(
            {'Problem': {'ErrorCode': 'PUBRI003', 'ErrorMessage': 'No result'}}, bd.request_result )

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
            self.patron_barcode, self.api_url_root, self.api_key, self.partnership_id, self.university_code )
        self.assertEqual(
            27, len(authentication_id) )

    def test_authorize(self):
        """ Tests authz session-extender. """
        a = Authenticator( self.logger )
        authentication_id = a.authenticate(
            self.patron_barcode, self.api_url_root, self.api_key, self.partnership_id, self.university_code )
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
        self.isbn_found_and_available = unicode( os.environ['BDPY_TEST__ISBN_FOUND_AND_AVAILABLE'] )
        self.isbn_found_and_unavailable = unicode( os.environ['BDPY_TEST__ISBN_FOUND_AND_UNAVAILABLE'] )
        self.isbn_not_found = unicode( os.environ['BDPY_TEST__ISBN_NOT_FOUND'] )

    def test_search_found_available(self):
        """ Tests basic isbn search for available found item. """
        s = Searcher( self.logger )
        ( search_key, search_value ) = ( 'ISBN', self.isbn_found_and_available )
        result_dct = s.search(
            self.patron_barcode, search_key, search_value, self.api_url_root, self.api_key, self.partnership_id, self.university_code )
        self.assertEqual(
            ['Available', 'PickupLocation', 'RequestLink', 'SearchTerm'], sorted(result_dct.keys()) )
        self.assertEqual(
            True, result_dct['Available'] )

    def test_search_found_unavailable(self):
        """ Tests basic isbn search for unavailable found item. """
        s = Searcher( self.logger )
        ( search_key, search_value ) = ( 'ISBN', self.isbn_found_and_unavailable )
        result_dct = s.search(
            self.patron_barcode, search_key, search_value, self.api_url_root, self.api_key, self.partnership_id, self.university_code )
        self.assertEqual(
            [u'Available', u'RequestLink', u'SearchTerm'], sorted(result_dct.keys()) )
        self.assertEqual(
            False, result_dct['Available'] )

    def test_search_not_found(self):
        """ Tests basic isbn search for not-found item. """
        s = Searcher( self.logger )
        ( search_key, search_value ) = ( 'ISBN', self.isbn_not_found )
        result_dct = s.search(
            self.patron_barcode, search_key, search_value, self.api_url_root, self.api_key, self.partnership_id, self.university_code )
        self.assertEqual(
            {"Problem":{"ErrorCode":"PUBFI002","ErrorMessage":"No result"}}, result_dct )

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
        self.isbn_found_and_available = unicode( os.environ['BDPY_TEST__ISBN_FOUND_AND_AVAILABLE'] )
        self.isbn_found_and_unavailable = unicode( os.environ['BDPY_TEST__ISBN_FOUND_AND_UNAVAILABLE'] )
        self.isbn_not_found = unicode( os.environ['BDPY_TEST__ISBN_NOT_FOUND'] )

    # def test_request_item_found_and_available(self):
    #     """ Tests basic isbn request for available found item.
    #         NOTE: commented out because this will really request the item. """
    #     r = Requester( self.logger )
    #     ( search_key, search_value ) = ( 'ISBN', self.isbn_found_and_available )
    #     result_dct = r.request_item(
    #         self.patron_barcode, search_key, search_value, self.pickup_location, self.api_url_root, self.api_key, self.partnership_id, self.university_code )
    #     self.assertEqual(
    #         ['RequestNumber'], sorted(result_dct.keys()) )
    #     self.assertEqual(
    #         'BRO-', result_dct['RequestNumber'][0:4] )

    def test_request_item_not_found(self):
        """ Tests basic isbn request for not-found item.
            NOTE: will really attempt a request. """
        r = Requester( self.logger )
        ( search_key, search_value ) = ( 'ISBN', self.isbn_not_found )
        result_dct = r.request_item(
            self.patron_barcode, search_key, search_value, self.pickup_location, self.api_url_root, self.api_key, self.partnership_id, self.university_code )
        self.assertEqual(
            {'Problem': {'ErrorCode': 'PUBRI003', 'ErrorMessage': 'No result'}}, result_dct )

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
