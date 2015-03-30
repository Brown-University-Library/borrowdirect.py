# -*- coding: utf-8 -*-

import json, pprint
import requests


class Searcher( object ):
    """ Enables easy calls to the BorrowDirect search webservice.
        BorrowDirect 'FindIt Web Service' docs: <http://borrowdirect.pbworks.com/w/page/90132998/FindItem%20Web%20Service> (login required)
        Called by BorrowDirect.run_search() """

    def __init__( self, logger ):
        self.logger = logger
        self.valid_search_keys = [ u'ISBN', u'ISSN', u'LCCN', u'OCLC', u'PHRASE' ]

    def search( self, patron_barcode, search_key, search_value, api_url_root, university_code, partnership_id ):
        """ Searches for exact key-value.
            Called by BorrowDirect.run_search() """
        assert search_key in self.valid_search_keys
        params = self.build_params( partnership_id, university_code, patron_barcode, search_key, search_value )
        url = u'%s/dws/item/available' % api_url_root
        headers = { u'Content-type': u'application/json' }
        r = requests.post( url, data=json.dumps(params), headers=headers )
        self.logger.debug( u'search r.content, `%s`' % r.content.decode(u'utf-8') )
        self.logger.debug( u'search r.url, `%s`' % r.url )
        result_dct = r.json()
        self.logger.debug( u'result_dct, `%s`' % pprint.pformat(result_dct) )
        return result_dct

    def build_params( self, partnership_id, university_code, patron_barcode, search_key, search_value ):
        """ Builds search json.
            Called by search() """
        params = {
            u'PartnershipId': partnership_id,
            # u'AuthorizationId': self.AId,
            u'Credentials': {
                u'LibrarySymbol': university_code, u'Barcode': patron_barcode },
            u'ExactSearch': [ {
                u'Type': search_key, u'Value': search_value } ]
            }
        self.logger.debug( u'params, `%s`' % pprint.pformat(params) )
        return params

    # end class Searcher
