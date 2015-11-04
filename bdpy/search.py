# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import json, pprint
import requests
from .auth import Authenticator


class Searcher( object ):
    """ Enables easy calls to the BorrowDirect search webservice.
        BorrowDirect 'FindIt Web Service' docs: <https://relais.atlassian.net/wiki/display/ILL/Find+Item>
        Called by BorrowDirect.run_search() """

    def __init__( self, logger ):
        self.logger = logger
        self.valid_search_keys = [ 'ISBN', 'ISSN', 'LCCN', 'OCLC', 'PHRASE' ]

    def search( self, patron_barcode, search_key, search_value, api_url_root, api_key, partnership_id, university_code ):
        """ Searches for exact key-value.
            Called by BorrowDirect.run_search() """
        assert search_key in self.valid_search_keys
        authorization_id = self.get_authorization_id( patron_barcode, api_url_root, api_key, university_code, partnership_id )
        params = self.build_params( partnership_id, university_code, patron_barcode, search_key, search_value )
        url = '%s/dws/item/available?aid=%s' % ( api_url_root, authorization_id )
        headers = { 'Content-type': 'application/json' }
        r = requests.post( url, data=json.dumps(params), headers=headers )
        self.logger.debug( 'search r.url, `%s`' % r.url )
        self.logger.debug( 'search r.content, `%s`' % r.content.decode('utf-8') )
        result_dct = r.json()
        return result_dct

    def get_authorization_id( self, patron_barcode, api_url_root, api_key, partnership_id, university_code ):
        """ Obtains authorization_id.
            Called by search()
            Note that only the authenticator webservice is called;
              the authorization webservice simply extends the same id's session time and so is not needed here. """
        self.logger.debug( 'starting get_authorization_id()...' )
        authr = Authenticator( self.logger )
        authorization_id = authr.authenticate(
            patron_barcode, api_url_root, api_key, university_code, partnership_id )
        return authorization_id

    def build_params( self, partnership_id, university_code, patron_barcode, search_key, search_value ):
        """ Builds search json.
            Called by search() """
        params = {
            'PartnershipId': partnership_id,
            'ExactSearch': [ {
                'Type': search_key, 'Value': search_value } ]
                }
        self.logger.debug( 'params, `%s`' % pprint.pformat(params) )
        return params

    # end class Searcher
