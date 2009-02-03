#!/usr/bin/env python
# encoding: utf-8
"""
test_siterouter.py

Created by Carlos Gabaldon on 2007-05-31.
Copyright (c) 2007 __MyCompanyName__. All rights reserved.
"""

import unittest
import person

class PersonTestCase(unittest.TestCase):
    def setUp(self):
        self.p = person.Person("Python", "Jack")
    def tearDown(self):
        self.p = None
        
    def testFirstName(self):
        assert self.p.first_name == "Python", "Wrong Name"
        
    def testLastName(self):
        assert self.p.last_name == "Jack", "Wrong Name"
        
if __name__ == "__main__":
    unittest.main()