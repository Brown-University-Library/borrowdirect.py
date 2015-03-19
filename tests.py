# -*- coding: utf-8 -*-

import imp, pprint, unittest
from bdpy import BorrowDirect


class BorrowDirectTests( unittest.TestCase ):

  def test_settings_instantiation(self):
    '''
    Tests that module instantiation handles settings not-defined, or defined as dict, module, or path.
    '''
    import exceptions, imp
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




if __name__ == "__main__":
  from bdpy import BorrowDirect
  unittest.main()
