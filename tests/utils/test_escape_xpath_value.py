import unittest

from AppiumLibrary.utils import escape_xpath_value

class EscapeXpathValueTests(unittest.TestCase):

    def test_no_quotes(self):
        self.assertEqual(escape_xpath_value("value"), "'value'")

    def test_single_quotes(self):
        self.assertEqual(escape_xpath_value("val'ue"), "\"val'ue\"")

    def test_double_quotes(self):
        self.assertEqual(escape_xpath_value('val"ue'), "'val\"ue'")

    def test_both_quotes(self):
        self.assertEqual(escape_xpath_value('val"u\'e'), "concat('val\"u', \"'\", 'e')")

    def test_multiple_single_and_double_quotes(self):
        self.assertEqual(escape_xpath_value('v"a\'l"u\'e'), "concat('v\"a', \"'\", 'l\"u', \"'\", 'e')")

    def test_empty_string(self):
        self.assertEqual(escape_xpath_value(""), "''")

    def test_integer(self):
        self.assertEqual(escape_xpath_value(123), "'123'")
