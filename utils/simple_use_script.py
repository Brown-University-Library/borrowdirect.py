# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os, pprint, time
from bdpy import BorrowDirect

""" Assumes bdpy has already been pip-installed, as per the main README.md """


print 'search example...'
search_defaults = {
    'API_URL_ROOT': unicode( os.environ['BDPY_SAMPLE_SCRIPT__API_URL_ROOT'] ),
    'API_KEY': unicode( os.environ['BDPY_SAMPLE_SCRIPT__API_KEY'] ),
    'PARTNERSHIP_ID': unicode( os.environ['BDPY_SAMPLE_SCRIPT__PARTNERSHIP_ID'] ),
    'UNIVERSITY_CODE': unicode( os.environ['BDPY_SAMPLE_SCRIPT__UNIVERSITY_CODE'] )
    }
bd = BorrowDirect( search_defaults )
patron_barcode = unicode( os.environ['BDPY_SAMPLE_SCRIPT__PATRON_BARCODE'] )
bd.run_search( patron_barcode, 'ISBN', '9780688002305' )
print 'search_result...'; pprint.pprint( bd.search_result )


print '---'; print ' '
time.sleep( 1 )  # being nice to the server


print 'request example...'
## Will really generate request if item is requestable
request_defaults = {
    'API_URL_ROOT': unicode( os.environ['BDPY_SAMPLE_SCRIPT__API_URL_ROOT'] ),
    'API_KEY': unicode( os.environ['BDPY_SAMPLE_SCRIPT__API_KEY'] ),
    'PARTNERSHIP_ID': unicode( os.environ['BDPY_SAMPLE_SCRIPT__PARTNERSHIP_ID'] ),
    'UNIVERSITY_CODE': unicode( os.environ['BDPY_SAMPLE_SCRIPT__UNIVERSITY_CODE'] ),
    'PICKUP_LOCATION': unicode( os.environ['BDPY_SAMPLE_SCRIPT__PICKUP_LOCATION'] )
    }
bd = BorrowDirect( request_defaults )
patron_barcode = unicode( os.environ['BDPY_SAMPLE_SCRIPT__PATRON_BARCODE'] )
bd.run_request_item( patron_barcode, 'ISBN', '9780688002305' )
print 'request_result...'; pprint.pprint( bd.request_result )
