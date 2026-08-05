import unittest

import mock

from AppiumLibrary import _ElementKeywords


class FindElementByClassNameTests(unittest.TestCase):

    def setUp(self):
        self.ek = _ElementKeywords()
        self.ek._info = mock.Mock()

    def test_find_by_index_returns_matching_element(self):
        elements = [mock.Mock(), mock.Mock(), mock.Mock()]
        self.ek._find_elements_by_class_name = mock.Mock(return_value=elements)
        self.ek._element_find = mock.Mock()

        result = self.ek._find_element_by_class_name('android.widget.TextView', 'index=1')

        self.assertIs(result, elements[1])
        self.ek._element_find.assert_not_called()

    def test_find_by_index_out_of_range_raises_value_error(self):
        self.ek._find_elements_by_class_name = mock.Mock(return_value=[mock.Mock()])

        with self.assertRaises(ValueError):
            self.ek._find_element_by_class_name('android.widget.TextView', 'index=5')

    def test_find_by_name_android_uses_xpath_fast_path(self):
        target = mock.Mock(text='Login')
        self.ek._get_platform = mock.Mock(return_value='android')
        self.ek._element_find = mock.Mock(return_value=target)
        self.ek._find_elements_by_class_name = mock.Mock()

        result = self.ek._find_element_by_class_name('android.widget.Button', 'Login')

        self.assertIs(result, target)
        self.ek._find_elements_by_class_name.assert_not_called()
        xpath_used = self.ek._element_find.call_args[0][0]
        self.assertIn("android.widget.Button[@text='Login']", xpath_used)

    def test_find_by_name_ios_uses_xpath_fast_path(self):
        target = mock.Mock(text='Login')
        self.ek._get_platform = mock.Mock(return_value='ios')
        self.ek._element_find = mock.Mock(return_value=target)
        self.ek._find_elements_by_class_name = mock.Mock()

        result = self.ek._find_element_by_class_name('XCUIElementTypeButton', 'Login')

        self.assertIs(result, target)
        self.ek._find_elements_by_class_name.assert_not_called()
        xpath_used = self.ek._element_find.call_args[0][0]
        self.assertIn("@label='Login' or @value='Login'", xpath_used)

    def test_find_by_name_falls_back_when_xpath_finds_nothing(self):
        matching = mock.Mock(text='Login')
        self.ek._get_platform = mock.Mock(return_value='android')
        self.ek._element_find = mock.Mock(return_value=None)
        self.ek._find_elements_by_class_name = mock.Mock(return_value=[mock.Mock(text='Other'), matching])

        result = self.ek._find_element_by_class_name('android.widget.Button', 'Login')

        self.assertIs(result, matching)

    def test_find_by_name_not_found_raises_value_error(self):
        self.ek._get_platform = mock.Mock(return_value='android')
        self.ek._element_find = mock.Mock(return_value=None)
        self.ek._find_elements_by_class_name = mock.Mock(return_value=[mock.Mock(text='Other')])

        with self.assertRaises(ValueError):
            self.ek._find_element_by_class_name('android.widget.Button', 'Login')

    def test_find_by_name_unsupported_platform_skips_xpath(self):
        matching = mock.Mock(text='Login')
        self.ek._get_platform = mock.Mock(return_value='windows')
        self.ek._element_find = mock.Mock()
        self.ek._find_elements_by_class_name = mock.Mock(return_value=[matching])

        result = self.ek._find_element_by_class_name('Button', 'Login')

        self.assertIs(result, matching)
        self.ek._element_find.assert_not_called()
