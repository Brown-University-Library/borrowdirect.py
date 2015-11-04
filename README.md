### about ###

'bdpy' faciliates programmatic access to the API to [BorrowDirect](http://www.borrowdirect.org), an academic book-borrowing consortium.

We use this in production for our 15,000+ successful automated BorrowDirect requests -- _and_ for thousands more automated searches for items that are either unavailable or not-found.

on this page...

- installation
- common usage
- notes
- license



### installation ###

    $ pip install git+https://github.com/birkin/borrowdirect.py@0.10

- best to install a 'release' version, as in the example above, though all code in the master branch can be expected to be stable.

- one dependency: the awesome [requests](http://docs.python-requests.org/en/latest/) module, which is automatically pip-installed if necessary



### common usage ###

- search:

        >>> from bdpy import BorrowDirect
        >>> defaults = {
            'API_URL_ROOT': url, 'API_KEY': key, 'PARTNERSHIP_ID': id, 'UNIVERSITY_CODE': code }
        >>> bd = BorrowDirect( defaults )
        >>> bd.run_search( patron_barcode, 'ISBN', '9780688002305' )
        >>> pprint( bd.search_result )

        ## if found and available via borrowdirect...
        {'Available': True,
         'PickupLocation': [{'PickupLocationCode': 'A',
                             'PickupLocationDescription': 'Rockefeller Library'}],
         'RequestLink': {'ButtonLabel': 'Request',
                         'ButtonLink': 'AddRequest',
                         'RequestMessage': 'Request this through Borrow Direct.'},
         'SearchTerm': 'isbn=9780688002305'}

        ## if found but not available via borrowdirect...
        {'Available': False,
         'RequestLink': {'ButtonLabel': 'View in the BROWN Library Catalog.',
                         'ButtonLink': 'http://josiah.brown.edu/record=.b18151139a',
                         'RequestMessage': 'This item is available locally.'}

        ## if not found
        {"Problem":{"ErrorCode":"PUBFI002","ErrorMessage":"No result"}}

- or request:

        >>> from bdpy import BorrowDirect
        >>> defaults = {
            'API_URL_ROOT': url, 'API_KEY': key, 'PARTNERSHIP_ID': id, 'UNIVERSITY_CODE': code, 'PICKUP_LOCATION': location }
        >>> bd = BorrowDirect( defaults )
        >>> bd.run_request_item( patron_barcode, 'ISBN', '9780688002305' )
        >>> pprint( bd.request_result )

        ## if found and available via borrowdirect...
        {'RequestNumber': 'BRO-12345678'}

        ## if found but not available via borrowdirect...
        {'RequestLink': {'ButtonLabel': 'View in the BROWN Library Catalog.',
                         'ButtonLink': 'http://josiah.brown.edu/record=.b18151139a',
                         'RequestMessage': 'This item is available locally.'}}

        ## if not found
        {u'Problem': {u'ErrorCode': u'PUBRI003', u'ErrorMessage': u'No result'}}



### notes ###

- BorrowDirect() instantiation is flexible: you can pass in a dict, a settings-module, a settings-module-path, or nothing (but then set the instance-attributes directly)

- no need to call the auth wrapper explicitly -- the calls to search and request do it automatically -- but you could if you wanted to:

        >>> from bdpy import BorrowDirect
        >>> defaults = { 'UNIVERSITY_CODE': the_code, 'API_URL_ROOT': the_url_root }
        >>> bd = BorrowDirect( defaults )
        >>> bd.run_auth_nz( a_patron_barcode )  # performs authN/Z & stores authorization-id
        >>> bd.AId  # authorization-id
        u'abc...'
        >>> bd.authnz_valid
        True

- BorrowDirect [api documentation](https://relais.atlassian.net/wiki/display/ILL/Relais+web+services)
    - [auth](https://relais.atlassian.net/wiki/display/ILL/Authentication)
    - [searching](https://relais.atlassian.net/wiki/display/ILL/Find+Item)
    - [requesting](https://relais.atlassian.net/wiki/display/ILL/RequestItem)

- bdpy code contact: birkin_diana@brown.edu

- check out [bdpyweb](https://github.com/birkin/bdpyweb_code), a lightweight [flask](http://flask.pocoo.org) app that turns this bdpy library into a webservice that can be accessed from any language. (This is how our automated [easyBorrow](http://library.brown.edu/borrowing/easyBorrow.php) system requests books for our patrons.)

- ruby [borrowdirect-api wrapper](https://github.com/jrochkind/borrow_direct)

- note: this code uses the November 2015 version of the Relais BorrowDirect api. To use this library with the previous version of the api:

        $ pip install git+https://github.com/birkin/borrowdirect.py@0.09b

    This is only a convenience of version-control; I'm not maintaining the code for the old BorrowDirect api.

- dev gotchas...
    - If you forget to include your partnership-id, you'll get back, on the auth-attempt, a message that your api-key is incorrect even if it's correct.
    - I've seen an instance where the search-api indicates, correctly, that an item is found but not available, because it's held and available locally -- _BUT_, the item _is_ requestable via the request-api. I have been told that anything successfully requested via the api will not be cancelled.



### license ###

The [MIT License](http://opensource.org/licenses/MIT) (MIT)

    Copyright (c) 2015 http://library.brown.edu/its/

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.

---

_( formatted in [markdown](http://daringfireball.net/projects/markdown/) )_
