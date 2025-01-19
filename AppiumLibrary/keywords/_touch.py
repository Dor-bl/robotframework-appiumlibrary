# -*- coding: utf-8 -*-

from AppiumLibrary.locators import ElementFinder
from .keywordgroup import KeywordGroup


class _TouchKeywords(KeywordGroup):

    def __init__(self):
        self._element_finder = ElementFinder()

    # Public, element lookups
    def zoom(self, locator, percent="200%", steps=1):
        """*DEPRECATED!!*
        Zooms in on an element a certain amount.
        """
        driver = self._current_application()
        element = self._element_find(locator, True, True)
        driver.zoom(element=element, percent=percent, steps=steps)

    def pinch(self, locator, percent="200%", steps=1):
        """*DEPRECATED!!* use `Execute Script` instead.
        Pinch in on an element a certain amount.
        """
        driver = self._current_application()
        element = self._element_find(locator, True, True)
        driver.pinch(element=element, percent=percent, steps=steps)

    def swipe(self, start_x, start_y, offset_x, offset_y, duration=1000):
        """
        Swipe from one point to another point, for an optional duration.

        Args:
         - start_x - x-coordinate at which to start
         - start_y - y-coordinate at which to start
         - offset_x - x-coordinate distance from start_x at which to stop
         - offset_y - y-coordinate distance from start_y at which to stop
         - duration - (optional) time to take the swipe, in ms.

        Usage:
        | Swipe | 500 | 100 | 100 | 0 | 1000 |

        _*NOTE: *_
        Android 'Swipe' is not working properly, use ``offset_x`` and ``offset_y`` as if these are destination points.
        """
        x_start = int(start_x)
        x_offset = int(offset_x)
        y_start = int(start_y)
        y_offset = int(offset_y)
        driver = self._current_application()
        driver.swipe(x_start, y_start, x_offset, y_offset, duration)

    def swipe_by_percent(self, start_x, start_y, end_x, end_y, duration=1000):
        """
        Swipe from one percent of the screen to another percent, for an optional duration.
        Normal swipe fails to scale for different screen resolutions, this can be avoided using percent.

        Args:
         - start_x - x-percent at which to start
         - start_y - y-percent at which to start
         - end_x - x-percent distance from start_x at which to stop
         - end_y - y-percent distance from start_y at which to stop
         - duration - (optional) time to take the swipe, in ms.

        Usage:
        | Swipe By Percent | 90 | 50 | 10 | 50 | # Swipes screen from right to left. |

        _*NOTE: *_
        This also considers swipe acts different between iOS and Android.

        New in AppiumLibrary 1.4.5
        """
        width = self.get_window_width()
        height = self.get_window_height()
        x_start = float(start_x) / 100 * width
        x_end = float(end_x) / 100 * width
        y_start = float(start_y) / 100 * height
        y_end = float(end_y) / 100 * height
        x_offset = x_end - x_start
        y_offset = y_end - y_start
        platform = self._get_platform()
        if platform == 'android':
            self.swipe(x_start, y_start, x_end, y_end, duration)
        else:
            self.swipe(x_start, y_start, x_offset, y_offset, duration)

    def scroll(self, start_locator, end_locator):
        """
        Scrolls from one element to another
        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.
        """
        el1 = self._element_find(start_locator, True, True)
        el2 = self._element_find(end_locator, True, True)
        driver = self._current_application()
        driver.scroll(el1, el2)

    def scroll_down(self, locator):
        """Scrolls down to element"""
        driver = self._current_application()
        element = self._element_find(locator, True, True)
        driver.execute_script("mobile: scroll", {"direction": 'down', 'elementid': element.id})

    def scroll_up(self, locator):
        """Scrolls up to element"""
        driver = self._current_application()
        element = self._element_find(locator, True, True)
        driver.execute_script("mobile: scroll", {"direction": 'up', 'elementid': element.id})

    def tap_with_positions(self, duration=500, *locations):
        """Taps on a particular place with up to five fingers, holding for a
        certain time

        Args:
        - locations - an array of tuples representing the x/y coordinates of
                the fingers to tap. Length can be up to five.
        - duration - length of time to tap, in ms. Default: 500ms

        Example:
        |  @{firstFinger}   |  create list  |  ${100}  |  ${500}  |
        |  @{secondFinger}  |  create list  |${700}    |  ${500}  |
        |  @{fingerPositions}  |  create list  |  ${firstFinger}  |  ${secondFinger}  |
        |  Sleep  |  1  |
        |  Tap with Positions  |  ${1000}  |  @{fingerPositions}  |

        New in AppiumLibrary v2
        """
        driver = self._current_application()
        driver.tap(positions=list(locations), duration=duration)
        
    def tap_with_number_of_taps(self, locator, number_of_taps, number_of_touches):
        """ Sends one or more taps with one or more touch points.iOS only.
        
        Args:
        - ``number_of_taps`` - The number of taps.
        - ``number_of_touches`` - The number of touch points.
        """
        driver = self._current_application()
        element = self._element_find(locator, True, True)
        params = {'element': element, 'numberOfTaps': number_of_taps, 'numberOfTouches': number_of_touches}
        driver.execute_script("mobile: tapWithNumberOfTaps", params)

    def click_alert_button(self, button_name):
        """ Clicks on Alert button identified by Name.iOS only.

        Args:
        - ``button_name`` - Text on the iOS alert button.

        Example:
        |  Click Alert Button  |  Allow  |

        New in AppiumLibrary v2
        """
        driver = self._current_application()
        params={'action': 'accept', 'buttonLabel': button_name}
        driver.execute_script("mobile: alert", params)

    def drag_and_drop(self, locator: str, target: str):
        """Drags the element identified by ``locator`` into the ``target`` element.

        The ``locator`` argument is the locator of the dragged element
        and the ``target`` is the locator of the target. See the
        `Locating elements` section for details about the locator syntax.

        Args:
        - ``origin`` - the element to drag
        - ``destination`` - the element to drag to

        Usage:
        | `Drag And Drop` | id=div#element | id=div.target |
        """
        element = self._element_find(locator, True, True)
        target = self._element_find(target, True, True)
        driver = self._current_application()
        driver.drag_and_drop(element, target)

    def flick(self, start_x:int, start_y:int, end_x:int, end_y:int):
        """Flick from one point to another point.

        Args:
        - ``start_x`` - x-coordinate at which to start
        - ``start_y`` - y-coordinate at which to start
        - ``end_x``   - x-coordinate at which to stop
        - ``end_y``   - y-coordinate at which to stop

        Usage:
        | Flick | 100 | 100 | 100 | 400 | # Flicks the screen up. |
        """
        driver = self._current_application()
        driver.flick(start_x, start_y, end_x, end_y)
