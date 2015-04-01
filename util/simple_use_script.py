# -*- coding: utf-8 -*-

""" Assumes bdpy has already been pip-installed, as per the main README.md """

import os, pprint, time
from bdpy import BorrowDirect


print u'search example...'
search_defaults = {
    u'UNIVERSITY_CODE': unicode( os.environ[u'BDPY_TEST__UNIVERSITY_CODE'] ),
    u'API_URL_ROOT': unicode( os.environ[u'BDPY_TEST__API_URL_ROOT'] ),
    u'PARTNERSHIP_ID': unicode( os.environ[u'BDPY_TEST__PARTNERSHIP_ID'] )
    }
bd = BorrowDirect( search_defaults )
patron_barcode = unicode( os.environ[u'BDPY_TEST__PATRON_BARCODE_GOOD'] )
bd.run_search( patron_barcode, u'ISBN', u'9780688002305' )
print u'search_result...'; pprint.pprint( bd.search_result )


print u'---'; print u' '
time.sleep( 2 )  # being nice to the test-server


print u'request example...'
## Be sure to use the TEST-server url, or you'll really generate a request!
request_defaults = {
    u'UNIVERSITY_CODE': unicode( os.environ[u'BDPY_TEST__UNIVERSITY_CODE'] ),
    u'API_URL_ROOT': unicode( os.environ[u'BDPY_TEST__API_URL_ROOT'] ),
    u'PARTNERSHIP_ID': unicode( os.environ[u'BDPY_TEST__PARTNERSHIP_ID'] ),
    u'PICKUP_LOCATION': unicode( os.environ[u'BDPY_TEST__PICKUP_LOCATION'] )
    }
bd = BorrowDirect( request_defaults )
patron_barcode = unicode( os.environ[u'BDPY_TEST__PATRON_BARCODE_GOOD'] )
bd.run_request_item( patron_barcode, u'ISBN', u'9780688002305' )
print u'request_result...'; pprint.pprint( bd.request_result )
