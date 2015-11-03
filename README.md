### about ###

'bdpy' faciliates programmatic access to the API to [BorrowDirect](http://www.borrowdirect.org), an academic book-borrowing consortium.

on this page...

- installation
- common usage
- notes
- license



### installation ###

    $ pip install git+https://github.com/birkin/borrowdirect.py@0.10dev

- best to install a 'release' version, as in the example above, though all code in the master branch can be expected to be stable.

- one dependency: the awesome [requests](http://docs.python-requests.org/en/latest/) module, which is automatically pip-installed if necessary



### common usage ###

- search:

        >>> from bdpy import BorrowDirect
        >>> defaults = { 'UNIVERSITY_CODE': the_code, 'API_URL_ROOT': the_url_root, 'PARTNERSHIP_ID': the_id }
        >>> bd = BorrowDirect( defaults )
        >>> bd.run_search( a_patron_barcode, 'ISBN', '9780688002305' )
        >>> sorted( bd.search_results['Item'].keys() )
        [u'AuthorizationId', u'Available', u'PickupLocations', u'SearchTerm']

- or request:

        >>> from bdpy import BorrowDirect
        >>> defaults = { 'UNIVERSITY_CODE': the_code, 'API_URL_ROOT': the_url_root, 'PARTNERSHIP_ID': the_id, 'PICKUP_LOCATION': the_location }
        >>> bd = BorrowDirect( defaults )
        >>> bd.run_request_item( a_patron_barcode, 'ISBN', '9780688002305' )
        >>> bd.request_result
        {u'Request': {u'RequestNumber': u'BRO-12345678'}}



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
    - [search](https://relais.atlassian.net/wiki/display/ILL/Find+Item)
    - [requesting](https://relais.atlassian.net/wiki/display/ILL/RequestItem)

- bdpy code contact: birkin_diana@brown.edu

- ruby [borrowdirect-api wrapper](https://github.com/jrochkind/borrow_direct)



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
