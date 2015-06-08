# -*- coding: utf-8 -*-

import json, pprint
import requests
from .auth import Authenticator


class Requester( object ):
    """ Enables easy calls to the BorrowDirect request webservice.
        BorrowDirect 'RequestItem Web Service' docs: <http://borrowdirect.pbworks.com/w/page/90133541/RequestItem%20Web%20Service> (login required)
        Called by BorrowDirect.run_request_item() """

    def __init__( self, logger ):
        self.logger = logger
        self.valid_search_keys = [ u'ISBN', u'ISSN', u'LCCN', u'OCLC', u'PHRASE' ]

    def request_item( self, search_key, search_value, pickup_location, api_url_root, patron_barcode, university_code, partnership_id ):
        """ Searches for exact key-value.
            Called by BorrowDirect.run_request_item() """
        assert search_key in self.valid_search_keys
        authorization_id = self.get_authorization_id( patron_barcode, api_url_root, university_code )
        params = self.build_params( partnership_id, authorization_id, pickup_location, search_key, search_value )
        url = u'%s/dws/item/add' % api_url_root
        headers = { u'Content-type': u'application/json' }
        r = requests.post( url, data=json.dumps(params), headers=headers )
        self.logger.debug( u'request r.url, `%s`' % r.url )
        self.logger.debug( u'request r.content, `%s`' % r.content.decode(u'utf-8') )
        result_dct = r.json()
        self.logger.debug( u'result_dct, `%s`' % pprint.pformat(result_dct) )
        return result_dct

    def get_authorization_id( self, patron_barcode, api_url_root, university_code ):
        """ Obtains authorization_id.
            Called by request_item()
            Note that only the authenticator webservice is called;
              the authorization webservice simply extends the same id's session time and so is not needed here. """
        authr = Authenticator( self.logger )
        authorization_id = authr.authenticate(
            patron_barcode, api_url_root, university_code )
        return authorization_id

    def build_params( self, partnership_id, authorization_id, pickup_location, search_key, search_value ):
        """ Builds request json.
            Called by request_item() """
        params = {
            u'PartnershipId': partnership_id,
            u'AuthorizationId': authorization_id,
            u'PickupLocation': pickup_location,
            u'Notes': u'',
            u'ExactSearch': [ {
                u'Type': search_key,
                u'Value': search_value
                } ]
            }
        self.logger.debug( u'params, `%s`' % pprint.pformat(params) )
        return params

    # end class Requester
