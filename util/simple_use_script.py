# -*- coding: utf-8 -*-

import os, pprint
from bdpy import BorrowDirect


search_defaults = {
    u'UNIVERSITY_CODE': unicode( os.environ[u'BDPY_TEST__UNIVERSITY_CODE'] ),
    u'API_URL_ROOT': unicode( os.environ[u'BDPY_TEST__API_URL_ROOT'] ),
    u'API_PARTNERSHIP_ID': unicode( os.environ[u'BDPY_TEST__PARTNERSHIP_ID'] )
    }
bd = BorrowDirect( search_defaults )
patron_barcode = unicode( os.environ[u'BDPY_TEST__PATRON_BARCODE_GOOD'] )
bd.run_search( patron_barcode, u'ISBN', u'9780688002305' )
print u'search_result...'; pprint.pprint( bd.search_result )
