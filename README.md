### about ###

'bdpy' faciliates programmatic access to the API to [BorrowDirect](http://www.borrowdirect.org), an academic book-borrowing consortium.

We use this in production for our 15,000+ successful automated BorrowDirect requests each year -- _and_ for thousands more automated searches for items that are either unavailable or not-found.

on this page...

- installation
- common usage
- possible responses
- notes
- license



### installation ###

git clone, or pip install...

    $ pip install git+https://github.com/Brown-University-Library/borrowdirect.py@0.10

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

        {'Available': True,
         'PickupLocation': [{'PickupLocationCode': 'A',
                             'PickupLocationDescription': 'Rockefeller Library'}],
         'RequestLink': {'ButtonLabel': 'Request',
                         'ButtonLink': 'AddRequest',
                         'RequestMessage': 'Request this through Borrow Direct.'},
         'SearchTerm': 'isbn=9780688002305'}


- or request:

        >>> from bdpy import BorrowDirect
        >>> defaults = {
            'API_URL_ROOT': url, 'API_KEY': key, 'PARTNERSHIP_ID': id, 'UNIVERSITY_CODE': code, 'PICKUP_LOCATION': location }
        >>> bd = BorrowDirect( defaults )
        >>> bd.run_request_item( patron_barcode, 'ISBN', '9780688002305' )
        >>> pprint( bd.request_result )

        {'RequestNumber': 'BRO-12345678'}



### possible responses ###

bd.search_result

    ## if found and available via borrowdirect...
    {'Available': True,
     'PickupLocation': [{'PickupLocationCode': 'A',
                         'PickupLocationDescription': 'Rockefeller Library'}],
     'RequestLink': {'ButtonLabel': 'Request',
                     'ButtonLink': 'AddRequest',
                     'RequestMessage': 'Request this through Borrow Direct.'},
     'SearchTerm': 'isbn=9780688002305'}

    ## found but held locally...
    {'Available': False,
     'RequestLink': {'ButtonLabel': 'View in the BROWN Library Catalog.',
                     'ButtonLink': 'http://josiah.brown.edu/record=.b18151139a',
                     'RequestMessage': 'This item is available locally.'}

    ## found but not available
    {'Available': False,
    'RequestLink': {'ButtonLabel': 'Request',
                   'ButtonLink': 'https://illiad.brown.edu/illiad/illiad.dll/OpenURL?genre=Book&sid=BD&HeldLocally=N&rft.title=The%20body%20and%20society&rft.aufirst=Peter%20Robert%20Lamont&rft.aulast=Brown&rft.edition=Twentieth%20anniversary%20ed.%20with%20a%20new%20introduction&rft.date=c2008&rft.isbn=9780231144063%20%28cloth%20%3A%20alk.%20paper%20%3A%20alk.%20paper%29&rft.isbn=9780231144070%20%28pbk.%20%3A%20alk.%20paper%20%3A%20alk.%20paper%29&rft.dat=195747707&rft.pub=Columbia%20University%20Press&rft.place=New%20York',
                   'RequestMessage': 'Place an interlibrary loan request via ILLiad.'},
    'SearchTerm': 'isbn=9780231144063'}

    ## if not found
    {"Problem":{"ErrorCode":"PUBFI002","ErrorMessage":"No result"}}

bd.request_result

    ## if found and available via borrowdirect...
    {'RequestNumber': 'BRO-12345678'}

    ## found but held locally...
    {'RequestLink': {'ButtonLabel': 'View in the BROWN Library Catalog.',
                     'ButtonLink': 'http://josiah.brown.edu/record=.b18151139a',
                     'RequestMessage': 'This item is available locally.'}}

    ## found but not available
    {'RequestLink': {'ButtonLabel': 'Request',
                      'ButtonLink': 'https://illiad.brown.edu/illiad/illiad.dll/OpenURL?genre=Book&sid=BD&HeldLocally=N&rft.title=The%20body%20and%20society&rft.aufirst=Peter%20Robert%20Lamont&rft.aulast=Brown&rft.edition=Twentieth%20anniversary%20ed.%20with%20a%20new%20introduction&rft.date=c2008&rft.isbn=9780231144063%20%28cloth%20%3A%20alk.%20paper%20%3A%20alk.%20paper%29&rft.isbn=9780231144070%20%28pbk.%20%3A%20alk.%20paper%20%3A%20alk.%20paper%29&rft.dat=195747707&rft.pub=Columbia%20University%20Press&rft.place=New%20York',
                      'RequestMessage': 'Place an interlibrary loan request via ILLiad.'}}

    ## if not found
    {u'Problem': {u'ErrorCode': u'PUBRI003', u'ErrorMessage': u'No result'}}



### notes ###

- BorrowDirect() instantiation is flexible: you can pass in a dict, a settings-module, a settings-module-path, or nothing (but then set the instance-attributes directly)

- no need to call the auth wrapper explicitly -- the calls to search and request do it automatically -- but you could if you wanted to:

        >>> from bdpy import BorrowDirect
        >>> defaults = {
            'API_URL_ROOT': url, 'API_KEY': key, 'PARTNERSHIP_ID': id, 'UNIVERSITY_CODE': code }
        >>> bd = BorrowDirect( defaults )
        >>> bd.run_auth_nz( patron_barcode )  # performs authN/Z & stores authorization-id
        >>> bd.AId  # authorization-id
        'abc...'
        >>> bd.authnz_valid
        True

- BorrowDirect [api documentation](https://relais.atlassian.net/wiki/display/ILL/Relais+web+services)
    - [auth](https://relais.atlassian.net/wiki/display/ILL/Authentication)
    - [searching](https://relais.atlassian.net/wiki/display/ILL/Find+Item)
    - [requesting](https://relais.atlassian.net/wiki/display/ILL/RequestItem)

- bdpy code contact: birkin_diana@brown.edu

- check out [bdpyweb](https://github.com/birkin/bdpyweb_code), a lightweight [flask](http://flask.pocoo.org) app that turns this bdpy library into a webservice that can be accessed from any language. (This is how our automated [easyBorrow](http://library.brown.edu/borrowing/easyBorrow.php) system requests books for our patrons.)

- for a ruby library, see [jonathan rochkind's](https://github.com/jrochkind) comprehensive and well-tested [borrowdirect-api wrapper](https://github.com/jrochkind/borrow_direct)

- note: this code uses the November 2015 version of the Relais BorrowDirect api. To use this library with the previous version of the api:

        $ pip install git+https://github.com/birkin/borrowdirect.py@0.09b

    This is only a convenience of version-control; I'm not maintaining the code for the old BorrowDirect api.

- dev gotchas...
    - If you forget to include your partnership-id, you'll get back, on the auth-attempt, a message that your api-key is incorrect even if it's correct.



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
