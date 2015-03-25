# -*- coding: utf-8 -*-

import json, pprint
import requests


class Authenticator( object ):
    """ Implements authentication & authorization.
        Called by BorrowDirect.run_auth_nz() """

    def __init__( self, logger ):
        self.logger = logger

    def authenticate( self, patron_barcode, authentication_url, university_code ):
        """ Accesses and returns authentication-id for storage.
            Called by BorrowDirect.run_auth_nz() """
        d = {
            u'AuthenticationInformation': {
            u'LibrarySymbol': university_code,
            u'PatronId': patron_barcode } }
        headers = { u'Content-type': u'application/json', u'Accept': u'text/plain'}
        r = requests.post( authentication_url, data=json.dumps(d), headers=headers )
        dct = r.json()
        authentication_id = dct[u'Authentication'][u'AuthnUserInfo'][u'AId']
        self.logger.debug( u'authentication_id, `%s`' % authentication_id )
        return authentication_id

    def authorize( self, authentication_url, authentication_id ):
        """ Checks authorization and extends authentication session time.
            Called by BorrowDirect.run_auth_nz() """
        url = u'%s?aid=%s' % ( authentication_url, authentication_id )
        r = requests.get( url )
        dct = r.json()
        state = dct[u'AuthorizationResult'][u'AuthorizationState'][u'State']  # boolean
        assert type( state ) == bool
        self.logger.debug( u'state, `%s`' % state )
        return state

    # end class Authenticator
