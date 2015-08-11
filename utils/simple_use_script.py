# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os, pprint, time
from bdpy import BorrowDirect

""" Assumes bdpy has already been pip-installed, as per the main README.md """


print 'search example...'
search_defaults = {
    'UNIVERSITY_CODE': unicode( os.environ['BDPY_TEST__UNIVERSITY_CODE'] ),
    'API_URL_ROOT': unicode( os.environ['BDPY_TEST__API_URL_ROOT'] ),
    'PARTNERSHIP_ID': unicode( os.environ['BDPY_TEST__PARTNERSHIP_ID'] )
    }
bd = BorrowDirect( search_defaults )
patron_barcode = unicode( os.environ['BDPY_TEST__PATRON_BARCODE'] )
bd.run_search( patron_barcode, 'ISBN', '9780688002305' )
print 'search_result...'; pprint.pprint( bd.search_result )


print '---'; print ' '
time.sleep( 2 )  # being nice to the test-server


print 'request example...'
## Be sure to use the TEST-server url, or you'll really generate a request!
request_defaults = {
    'UNIVERSITY_CODE': unicode( os.environ['BDPY_TEST__UNIVERSITY_CODE'] ),
    'API_URL_ROOT': unicode( os.environ['BDPY_TEST__API_URL_ROOT'] ),
    'PARTNERSHIP_ID': unicode( os.environ['BDPY_TEST__PARTNERSHIP_ID'] ),
    'PICKUP_LOCATION': unicode( os.environ['BDPY_TEST__PICKUP_LOCATION'] )
    }
bd = BorrowDirect( request_defaults )
patron_barcode = unicode( os.environ['BDPY_TEST__PATRON_BARCODE'] )
bd.run_request_item( patron_barcode, 'ISBN', '9780688002305' )
print 'request_result...'; pprint.pprint( bd.request_result )
