# -*- coding: utf-8 -*-

import json, pprint
import requests


class Authenticator( object ):
    """ Enables easy calls to the BorrowDirect authN/Z webservices.
        BorrowDirect 'Authentication Web Service' docs: <http://borrowdirect.pbworks.com/w/page/90132761/Authentication%20Web%20Service> (login required)
        BorrowDirect 'Authorization Web Service' docs: <http://borrowdirect.pbworks.com/w/page/90132884/Authorization%20Web%20Service> (login required)
        Called by BorrowDirect.run_auth_nz() """

    def __init__( self, logger ):
        self.logger = logger

    def authenticate( self, patron_barcode, api_url, university_code ):
        """ Accesses and returns authentication-id for storage.
            Called by BorrowDirect.run_auth_nz() """
        d = {
            u'AuthenticationInformation': {
            u'LibrarySymbol': university_code,
            u'PatronId': patron_barcode } }
        headers = { u'Content-type': u'application/json', u'Accept': u'text/plain'}
        url = u'%s/portal-service/user/authentication/patron' % api_url
        r = requests.post( url, data=json.dumps(d), headers=headers )
        dct = r.json()
        authentication_id = dct[u'Authentication'][u'AuthnUserInfo'][u'AId']
        self.logger.debug( u'authentication_id, `%s`' % authentication_id )
        return authentication_id

    def authorize( self, api_url, authentication_id ):
        """ Checks authorization and extends authentication session time.
            Called by BorrowDirect.run_auth_nz() """
        url = u'%s/portal-service/user/authz/isAuthorized?aid=%s' % ( api_url, authentication_id )
        r = requests.get( url )
        dct = r.json()
        state = dct[u'AuthorizationResult'][u'AuthorizationState'][u'State']  # boolean
        assert type( state ) == bool
        self.logger.debug( u'state, `%s`' % state )
        return state

    # end class Authenticator
