"""
Tests a list of ISBNs.

- Load ISBNs
- confirm redis is running
- enqueue the jobs

each job:
- hit bdpy test-server search, store result to redis
- hit bdpy test-server request, store result to redis
"""

import json, os
import redis, rq


class EnqueueIsbnTestJobs( object ):
    """ Loads up queue. """

    def __init__( self ):
        """ Sets vars & ensures environment is ready. """
        self.ISBN_JSON = os.environ[u'BD_ISBN_TEST__JSON_PATH']
        self.QUEUE_NAME = u'BD_ISBN_TEST'
        self.HASH_KEY = u'BD_ISBN_TEST'
        self.r = redis.StrictRedis( host=u'localhost', port=6379, db=0 )
        self.q = rq.Queue( QUEUE_NAME, connection=redis.Redis() )
        assert len( self.r.keys() ) > -1  # if redis isn't running this will generate an error
        assert self.r.get( HASH_KEY ) == None  # ensures key isn't being used

    def enqueue_isbn_test_jobs( self ):
        """ Calls functions to enqueue jobs.
            Called by run_enqueue_isbn_test_jobs() """
        unique_isbns = self.load_isbns()
        self.enqueue( unique_isbns )
        return

    def load_isbns( self ):
        """ Loads isbns from a json file.
            Called by enqueue_isbn_test_jobs() """
        with open( ISBN_JSON ) as f:
            utf8_txt = f.read()
            isbns = json.loads( utf8_txt )
        isbns = sorted( isbns )
        print u'- num_isbns is `%s`' % len( isbns )
        isbns_set = set( mylist )
        unique_isbns = list( isbns_set )
        unique_isbns = sorted( unique_isbns )
        print u'- num_unique_isbns is `%s`' % len( unique_isbns )
        return unique_isbns

    def enqueue( self, unique_isbns ):
        """ Enqueues jobs.
            Called by enqueue_isbn_test_jobs() """
        for isbn in unique_isbns:
            q.enqueue_call(
                func=u'bdpy.utils.run_isbn_test',
                kwargs={ u'isbn': isbn },
                timeout=600 )  # 10 minutes
        return

    # end class EnqueueIsbnTestJobs


class IsbnTest( object ):
    """ Hits bd-api test-server with a search, and then a request, and stores output in redis for later review. """

    def __init__( self ):
        pass

    def do_search( self ):
        pass

    def do_request( self ):
        pass

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
    it = IsbnTest( isbn )
    it.do_search()
    it.do_request()
    return
