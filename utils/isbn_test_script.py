"""
Tests a json-file list of ISBNs.

- Loads ISBNs
- confirms redis is running
- enqueues the jobs

each job:
- hits bdpy test-server search, stores result to redis
- hits bdpy test-server request, stores result to redis

Assumes bdpy has already been pip-installed, as per the main README.md
Assumes redis and rq have already been pip-installed
"""

import datetime, json, os, time
import redis, rq
from bdpy import BorrowDirect


class EnqueueIsbnTestJobs( object ):
    """ Loads up queue. """

    def __init__( self ):
        """ Sets vars & ensures environment is ready. """
        self.ISBN_JSON = os.environ[u'BD_ISBN_TEST__JSON_PATH']
        self.QUEUE_NAME = u'BD_ISBN_TEST'
        self.HASH_KEY = u'BD_ISBN_TEST'
        self.r = redis.StrictRedis( host=u'localhost', port=6379, db=0 )
        self.q = rq.Queue( self.QUEUE_NAME, connection=self.r )
        assert len( self.r.keys() ) > -1  # if redis isn't running this will generate an error
        assert self.r.get( self.HASH_KEY ) == None  # ensures key isn't being used

    def enqueue_isbn_test_jobs( self ):
        """ Calls functions to enqueue jobs.
            Called by run_enqueue_isbn_test_jobs() """
        unique_isbns = self.load_isbns()
        self.enqueue( unique_isbns )
        return

    def load_isbns( self ):
        """ Loads isbns from a json file.
            Called by enqueue_isbn_test_jobs() """
        with open( self.ISBN_JSON ) as f:
            utf8_txt = f.read()
            isbns = json.loads( utf8_txt )
        isbns = sorted( isbns )
        print u'- num_isbns is `%s`' % len( isbns )
        isbns_set = set( isbns )
        unique_isbns = list( isbns_set )
        unique_isbns = sorted( unique_isbns )
        print u'- num_unique_isbns is `%s`' % len( unique_isbns )
        return unique_isbns

    def enqueue( self, unique_isbns ):
        """ Enqueues jobs.
            Called by enqueue_isbn_test_jobs()
            Assumes rq worker is started at ../utils """
        for isbn in unique_isbns:
            self.q.enqueue_call(
                func=u'utils.isbn_test_script.run_perform_test',
                kwargs={ u'isbn': isbn },
                timeout=600 )  # 10 minutes
        return

    # end class EnqueueIsbnTestJobs


class IsbnTest( object ):
    """ Hits bd-api test-server with a search, and then a request, and stores output in redis for later review. """

    def __init__( self ):
        self.HASH_KEY = u'BD_ISBN_TEST'
        self.search_defaults = {
            u'UNIVERSITY_CODE': unicode( os.environ[u'BDPY_TEST__UNIVERSITY_CODE'] ),
            u'API_URL_ROOT': unicode( os.environ[u'BDPY_TEST__API_URL_ROOT'] ),
            u'PARTNERSHIP_ID': unicode( os.environ[u'BDPY_TEST__PARTNERSHIP_ID'] ) }
        self.request_defaults = {
            u'UNIVERSITY_CODE': unicode( os.environ[u'BDPY_TEST__UNIVERSITY_CODE'] ),
            u'API_URL_ROOT': unicode( os.environ[u'BDPY_TEST__API_URL_ROOT'] ),
            u'PARTNERSHIP_ID': unicode( os.environ[u'BDPY_TEST__PARTNERSHIP_ID'] ),
            u'PICKUP_LOCATION': unicode( os.environ[u'BDPY_TEST__PICKUP_LOCATION'] ) }
        self.patron_barcode = unicode( os.environ[u'BDPY_TEST__PATRON_BARCODE_GOOD'] )


    def do_search( self, isbn ):
        """ Performs bd-api search; stores result.
            Called by run_perform_test() """
        time.sleep( 2 )
        bd = BorrowDirect( self.search_defaults )
        start = datetime.datetime.now()
        bd.run_search( self.patron_barcode, u'ISBN', isbn )
        end = datetime.datetime.now()
        time_taken = unicode( end-start )
        dct = { u'search_result': {
            u'result': bd.search_result, u'time_taken': time_taken} }
        self.store_results( isbn, dct )
        return

    def do_request( self, isbn ):
        """ Performs bd-api request on test-server; stores result.
            Called by run_perform_test() """
        time.sleep( 2 )
        bd = BorrowDirect( self.request_defaults )
        start = datetime.datetime.now()
        bd.run_request_item( self.patron_barcode, u'ISBN', isbn )
        end = datetime.datetime.now()
        time_taken = unicode( end-start )
        dct = { u'request_result': {
            u'result': bd.request_result, u'time_taken': time_taken} }
        self.store_results( isbn, dct )
        return

    def store_results( self, isbn, dct ):
        """ Stores results to redis.
            Called by do_search() and do_request() """
        rds = redis.StrictRedis( host=u'localhost', port=6379, db=0 )
        if dct.keys()[0] == u'search_result':
            rds.hset( self.HASH_KEY, isbn, json.dumps(dct) )
        elif dct.keys()[0] == u'request_result':
            search_result = json.loads( rds.hget(self.HASH_KEY, isbn) )[u'search_result']
            full_dct = { u'search_result': search_result, u'request_result': dct[u'request_result'] }
            rds.hset( self.HASH_KEY, isbn, json.dumps(full_dct) )
        return

    # end class IsbnTest


## runners

def run_enqueue_isbn_test_jobs():
    """ Prepares list of isbns to test & enqueues jobs.
        Called manually. """
    e = EnqueueIsbnTestJobs()
    e.enqueue_isbn_test_jobs()
    return

def run_perform_test( isbn ):
    """ Calls perform_test()
        Called manually. """
    it = IsbnTest()
    it.do_search( isbn )
    it.do_request( isbn )
    return
