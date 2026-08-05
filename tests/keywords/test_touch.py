import unittest
import sys
from unittest import mock

class TouchKeywordsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create mocks for all missing dependencies
        def create_mock_package(name):
            m = mock.Mock()
            m.__path__ = []
            m.__spec__ = mock.Mock()
            return m

        cls.mocks = {
            'six': mock.Mock(),
            'decorator': mock.Mock(),
            'robot': create_mock_package('robot'),
            'robot.api': create_mock_package('robot.api'),
            'robot.libraries': create_mock_package('robot.libraries'),
            'robot.utils': create_mock_package('robot.utils'),
            'robot.libraries.BuiltIn': mock.Mock(),
            'robot.api.logger': mock.Mock(),
            'appium': create_mock_package('appium'),
            'appium.webdriver': create_mock_package('appium.webdriver'),
            'appium.webdriver.extensions': create_mock_package('appium.webdriver.extensions'),
            'appium.webdriver.extensions.action_helpers': mock.Mock(),
            'appium.webdriver.common': create_mock_package('appium.webdriver.common'),
            'appium.webdriver.common.appiumby': create_mock_package('appium.webdriver.common.appiumby'),
            'appium.options': create_mock_package('appium.options'),
            'appium.options.common': create_mock_package('appium.options.common'),
            'appium.webdriver.client_config': create_mock_package('appium.webdriver.client_config'),
            'selenium': create_mock_package('selenium'),
            'selenium.webdriver': create_mock_package('selenium.webdriver'),
            'selenium.webdriver.remote': create_mock_package('selenium.webdriver.remote'),
            'selenium.webdriver.remote.webelement': create_mock_package('selenium.webdriver.remote.webelement'),
            'selenium.webdriver.common': create_mock_package('selenium.webdriver.common'),
            'selenium.webdriver.common.actions': create_mock_package('selenium.webdriver.common.actions'),
            'selenium.webdriver.common.actions.action_builder': create_mock_package('selenium.webdriver.common.actions.action_builder'),
            'selenium.webdriver.common.actions.interaction': create_mock_package('selenium.webdriver.common.actions.interaction'),
            'selenium.webdriver.common.actions.pointer_input': create_mock_package('selenium.webdriver.common.actions.pointer_input'),
            'selenium.common': create_mock_package('selenium.common'),
            'selenium.common.exceptions': create_mock_package('selenium.common.exceptions'),
            'geopy': create_mock_package('geopy'),
            'geopy.geocoders': create_mock_package('geopy.geocoders'),
        }

        cls.mocks['six'].with_metaclass = lambda meta, *bases: type('with_metaclass', bases, {})
        cls.mocks['robot.utils'].ConnectionCache = mock.Mock()
        cls.mocks['appium.webdriver.common.appiumby'].AppiumBy = mock.Mock()
        cls.mocks['appium.options.common'].AppiumOptions = mock.Mock()
        cls.mocks['appium.webdriver.client_config'].AppiumClientConfig = mock.Mock()
        cls.mocks['selenium.webdriver.remote.webelement'].WebElement = mock.Mock()
        cls.mocks['selenium.webdriver.common.actions.action_builder'].ActionBuilder = mock.Mock()
        cls.mocks['selenium.webdriver.common.actions.interaction'].POINTER_TOUCH = mock.Mock()
        cls.mocks['selenium.webdriver.common.actions.pointer_input'].PointerInput = mock.Mock()
        cls.mocks['selenium.common.exceptions'].WebDriverException = type('WebDriverException', (Exception,), {})
        cls.mocks['geopy.geocoders'].Nominatim = mock.Mock()

        cls.sys_modules_patcher = mock.patch.dict(sys.modules, cls.mocks)
        cls.sys_modules_patcher.start()

        # Import the class under test
        from AppiumLibrary.keywords._touch import _TouchKeywords
        cls._TouchKeywords = _TouchKeywords

    @classmethod
    def tearDownClass(cls):
        cls.sys_modules_patcher.stop()

    def setUp(self):
        self.tk = self._TouchKeywords()
        self.tk._current_application = mock.Mock()
        self.tk._element_find = mock.Mock()

    def test_tap_with_number_of_taps(self):
        driver = self.tk._current_application.return_value
        element = mock.Mock()
        element.id = 'some_id'
        self.tk._element_find.return_value = element

        self.tk.tap_with_number_of_taps('id=my_element', 2, 1)

        expected_params = {
            'element': element,
            'numberOfTaps': 2,
            'numberOfTouches': 1
        }
        driver.execute_script.assert_called_with("mobile: tapWithNumberOfTaps", expected_params)

    def test_tap_with_number_of_taps_missing_element(self):
        self.tk._element_find.side_effect = ValueError("Element not found")

        with self.assertRaises(ValueError):
            self.tk.tap_with_number_of_taps('id=non_existent', 1, 1)
