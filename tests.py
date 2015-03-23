# -*- coding: utf-8 -*-

import exceptions, imp, pprint, unittest
from bdpy import BorrowDirect


class BorrowDirectTests( unittest.TestCase ):

    def test_settings_instantiation(self):
        """ Tests that module instantiation handles settings not-defined, or defined as dict, module, or path. """
        ## no settings passed on instantiation
        bd = BorrowDirect()  # no settings info
        self.assertEqual(
            True, isinstance(bd, BorrowDirect) )
        ## dict settings
        settings_dict = {}  ## test empty
        bd = BorrowDirect( settings_dict )
        self.assertEqual(
            None, bd.UNIVERSITY_CODE )
        settings_dict = { u'UNIVERSITY_CODE': u'123' }  ## test populated
        bd = BorrowDirect( settings_dict )
        self.assertEqual(
            u'123', bd.UNIVERSITY_CODE )
        ## module settings
        s = imp.new_module( u'settings' )  ## test empty
        bd = BorrowDirect( s )
        self.assertEqual(
            None, bd.UNIVERSITY_CODE )
        s = imp.new_module( u'settings' )  ## test populated
        s.UNIVERSITY_CODE = u'234'
        bd = BorrowDirect( s )
        self.assertEqual(
            u'234', bd.UNIVERSITY_CODE )
        ## TODO: test settings path

    def test_run_auth_nz(self):
        """ Tests successful and unsucessful authN/Z. """
        bd = BorrowDirect()
        bd.run_auth_nz()
        self.assertEqual(
            True, bd.auth_nz_valid )




if __name__ == "__main__":
  from bdpy import BorrowDirect
  unittest.main()
