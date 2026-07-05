import unittest
from unittest import mock
from AppiumLibrary.keywords._element import _ElementKeywords

class ElementKeywordsTests(unittest.TestCase):

    @mock.patch('AppiumLibrary.keywords._element.BuiltIn')
    @mock.patch('AppiumLibrary.keywords._element.ElementFinder')
    def test_element_should_be_disabled_success(self, mock_element_finder, mock_builtin):
        element_kw = _ElementKeywords()
        element_kw._info = mock.Mock()
        element_kw.log_source = mock.Mock()
        element_kw._element_find = mock.Mock()

        mock_element = mock.Mock()
        mock_element.is_enabled.return_value = False
        element_kw._element_find.return_value = mock_element

        element_kw.element_should_be_disabled('locator')

        element_kw._element_find.assert_called_once_with('locator', True, True)
        mock_element.is_enabled.assert_called_once()
        element_kw.log_source.assert_not_called()
        element_kw._info.assert_called_once_with("Element 'locator' is disabled .")

    @mock.patch('AppiumLibrary.keywords._element.BuiltIn')
    @mock.patch('AppiumLibrary.keywords._element.ElementFinder')
    def test_element_should_be_disabled_failure(self, mock_element_finder, mock_builtin):
        element_kw = _ElementKeywords()
        element_kw._info = mock.Mock()
        element_kw.log_source = mock.Mock()
        element_kw._element_find = mock.Mock()

        mock_element = mock.Mock()
        mock_element.is_enabled.return_value = True
        element_kw._element_find.return_value = mock_element

        with self.assertRaisesRegex(AssertionError, "Element 'locator' should be disabled but did not"):
            element_kw.element_should_be_disabled('locator')

        element_kw._element_find.assert_called_once_with('locator', True, True)
        mock_element.is_enabled.assert_called_once()
        element_kw.log_source.assert_called_once_with('INFO')
        element_kw._info.assert_not_called()

if __name__ == '__main__':
    unittest.main()
