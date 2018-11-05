#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import unittest
import inflect


class TestUnicode(unittest.TestCase):
    """ Unicode compatibility test cases """

    def test_unicode_plural(self):
        """ Unicode compatibility test cases for plural """
        engine = inflect.engine()
        unicode_test_cases = {"cliché": "clichés", "ångström": "ångströms"}
        for singular, plural in unicode_test_cases.items():
            self.assertEqual(plural, engine.plural(singular))
