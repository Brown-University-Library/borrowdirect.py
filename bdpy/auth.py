# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import json, pprint
import requests


class Authenticator( object ):
    """ Enables easy calls to the BorrowDirect authN/Z webservices.
        BorrowDirect 'Authentication Web Service' docs: <http://borrowdirect.pbworks.com/w/page/90132761/Authentication%20Web%20Service> (login required)
        BorrowDirect 'Authorization Web Service' docs: <http://borrowdirect.pbworks.com/w/page/90132884/Authorization%20Web%20Service> (login required)
        Called by BorrowDirect.run_auth_nz() """

    def __init__( self, logger ):
        self.logger = logger

    def authenticate( self, patron_barcode, api_url, api_key, university_code, partnership_id ):
        """ Accesses and returns authentication-id for storage.
            Called by BorrowDirect.run_auth_nz(), Searcher.get_authorization_id(), and Requester.get_authorization_id() """
        url = '%s/portal-service/user/authentication' % api_url
        headers = { 'Content-type': 'application/json', 'Accept': 'text/plain'}
        params = {
            'ApiKey': api_key,
            'UserGroup': 'patron',
            'LibrarySymbol': university_code,
            'PartnershipId': partnership_id,
            'PatronId': patron_barcode }
        r = requests.post( url, data=json.dumps(params), headers=headers )
        authentication_id = r.json()['AuthorizationId']
        return authentication_id

    def authorize( self, api_url, authentication_id ):
        """ Checks authorization and extends authentication session time.
            Called by BorrowDirect.run_auth_nz() """
        url = '%s/portal-service/user/authz/isAuthorized?aid=%s' % ( api_url, authentication_id )
        r = requests.get( url )
        dct = r.json()
        state = dct['AuthorizationState']['State']  # boolean
        assert type( state ) == bool
        return state

    # end class Authenticator
