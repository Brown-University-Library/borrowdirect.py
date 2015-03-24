# -*- coding: utf-8 -*-

import json, pprint
import requests


class Authenticator( object ):
    """ Implements authentication & authorization. """

    def __init__( self, logger ):
        self.logger = logger

    def authenticate( self, patron_barcode, auth_url, university_code ):
        """ Runs authN/Z and stores authentication-id.
            Called manually. """
        self.logger.debug( u'starting...' )
        self.logger.debug( u'url, `%s`' % auth_url )
        ## authn - get the borrowdirect authentication-id
        d = {
            u'AuthenticationInformation': {
            u'LibrarySymbol': university_code,
            u'PatronId': patron_barcode } }
        self.logger.debug( u'params-dict, `%s`' % pprint.pformat(d) )
        headers = { u'Content-type': u'application/json', u'Accept': u'text/plain'}
        r = requests.post( auth_url, data=json.dumps(d), headers=headers )
        self.logger.debug( u'r.content, `%s`' % r.content.decode(u'utf-8') )
        self.logger.debug( u'r.status_code, `%s`' % r.status_code )
        dct = r.json()
        self.logger.debug( u'response dct, `%s`' % pprint.pformat(dct) )
        authentication_id = dct[u'Authentication'][u'AuthnUserInfo'][u'AId']
        # authentication_id = u'foo'
        self.logger.debug( u'authentication_id, `%s`' % authentication_id )
        return authentication_id
