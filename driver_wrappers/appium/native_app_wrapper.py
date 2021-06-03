import time
from factory.handling.assertion import Assertion as Assert
from factory.handling.running_exception import RunningException as Rexc
from factory.singleton_web_driver import WebDriver
from appium.webdriver.common.mobileby import MobileBy as MBy
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support.ui import Select
from factory.utils.StringsUtil import StringUtil as String
from factory.utils.DataEncryptedUtil import DataEncrypted as RandomData


ELEMENT_LOCATION = "/html/body"
driver = WebDriver.use()


class BaseAppPage(WebDriver):
    @staticmethod
    def assert_that(comparative_value=""):
        return Assert(comparative_value)

    def scroll_into_view(self, by_type, element_location):
        self.wait_for_element(by_type, element_location)
        WebDriver.use().execute_script("mobile: scroll", {"direction": "down"})
        return self

    def drag_to_view(self, by_type, element_location):
        self.wait_for_element(by_type, element_location)
        element_to_tap = BaseAppPage.use().find_element_by_xpath(element_location)
        element_to_drag_to = BaseAppPage.use().find_element_by_xpath()
        WebDriver.use().driver.scroll(element_to_tap, element_to_drag_to)
        return self

    @staticmethod
    def hide_keyboard():
        WebDriver.use().hide_keyboard()

    def accept_alert(self):
        try:
            time.sleep(1)
            WebDriver.use().switch_to_alert().accept()
        except:
            WebDriver.use().execute_script("mobile: acceptAlert")
        return self

    def cancel_alert(self):
        try:
            time.sleep(1)
            WebDriver.use().switch_to_alert().dismiss()
        except:
            WebDriver.use().execute_script("mobile: dismissAlert")
        return self

    def is_the_element_presented(self, by_type, element_location, timeout=30):
        self.get_page_to_load()
        return self.wait_for_element(
            by_type, element_location, is_presented=True, handle_timeout=timeout
        )

    def accept_notification(self, by_type, element_location):
        try:
            self.wait_for_element(by_type, element_location, handle_timeout=3)
        except:
            pass
        finally:
            if self.is_the_element_presented(by_type, element_location, timeout=2) is False:
                pass
            else:
                self.click_on(by_type, element_location, timeout=2)
                try:
                    self.accept_alert()
                except:
                    self.click_on(by_type, element_location, timeout=2)
        return self

    @staticmethod
    def get_element_text(by_type, element_location, is_visible=False):
        element_location = str(element_location)
        try:
            BaseAppPage.wait_for_element(by_type, element_location, is_visible=is_visible)
            element = BaseAppPage.get_element_by(by_type, element_location)
            try:
                BaseAppPage.wait_for_element(by_type, element_location, is_presented=True)
                text = WebDriver.execute_javascript("return arguments[0].textContent", element)
                return text
            except:
                text = str(element.text).strip()
                return text
        except ValueError as ve:
            Rexc.raise_assertion_error(
                f"The element '{element_location}' does not match the text value expected! ", ve
            )

    @staticmethod
    def type_text(
        input_text,
        by_type,
        element_location,
        is_clickable=False,
        clear_field=False,
        hide_keyboard=True,
    ):
        if BaseAppPage.is_not_empty_value(input_text):
            try:
                if String.is_not_blank_or_null(input_text):
                    BaseAppPage.wait_for_element(
                        by=by_type,
                        location=element_location,
                        is_visible=True,
                        is_clickable=is_clickable,
                    )
                    element = BaseAppPage.get_element_by(by_type, element_location)
                    input_text_formatted = BaseAppPage.generate_random_string_data(input_text)
                    if clear_field:
                        element.clear()
                    element.send_keys(str(input_text_formatted))
                    if hide_keyboard:
                        BaseAppPage.hide_keyboard()
            except ValueError as ve:
                Rexc.raise_assertion_error(
                    f"The element '{element_location}' is not iterable or value {input_text} not matches! ",
                    ve,
                )

    @staticmethod
    def click_on(
        by_type="",
        element_location="",
        is_visible=False,
        by_id=False,
        by_xpath=False,
        by_css_selector=False,
        by_name=False,
        by_tagname=False,
        by_classname=False,
        by_custom=False,
        by_accessibility_id=False,
        by_ios_uiautomation=False,
        by_android_uiautomator=False,
        by_android_viewtag=False,
        by_ios_class_chain=False,
        by_ios_predicate=False,
        by_image=False,
        timeout=30,
    ):
        BaseAppPage.wait_for_element(
            by_type,
            element_location,
            is_visible=is_visible,
            is_clickable=True,
            handle_timeout=timeout,
        )
        if by_type != "":
            element = BaseAppPage.get_element_by(by_type, element_location)
            if element.is_displayed():
                try:
                    BaseAppPage.get_element_by(by_type, element_location).click()
                except:
                    BaseAppPage.get_element_by(by_type, element_location).click()
                finally:
                    BaseAppPage.log_action(element_location, action_name="Click")
        else:
            BaseAppPage.click_on_element_by_id(element_location)
            fetch_and_click = (
                lambda click_method, by_type_state: click_method if by_type_state is True else False
            )
            fetch_and_click(BaseAppPage.click_on_element_by_id(element_location), by_id)
            fetch_and_click(BaseAppPage.click_on_element_by_xpath(element_location), by_xpath)
            fetch_and_click(
                BaseAppPage.click_on_element_by_css_selector(element_location), by_css_selector
            )
            fetch_and_click(BaseAppPage.click_on_element_by_name(element_location), by_name)
            fetch_and_click(BaseAppPage.click_on_element_by_tag_name(element_location), by_tagname)
            fetch_and_click(
                BaseAppPage.click_on_element_by_class_name(element_location), by_classname
            )
            fetch_and_click(BaseAppPage.click_on_element_by_custom(element_location), by_custom)
            fetch_and_click(
                BaseAppPage.click_on_element_by_accessibility_id(element_location),
                by_accessibility_id,
            )
            fetch_and_click(
                BaseAppPage.click_on_element_by_ios_uiautomation(element_location),
                by_ios_uiautomation,
            )
            fetch_and_click(
                BaseAppPage.click_on_element_by_android_uiautomator(element_location),
                by_android_uiautomator,
            )
            fetch_and_click(
                BaseAppPage.click_on_element_by_android_viewtag(element_location),
                by_android_viewtag,
            )
            fetch_and_click(
                BaseAppPage.click_on_element_by_ios_class_chain(element_location),
                by_ios_class_chain,
            )
            fetch_and_click(
                BaseAppPage.click_on_element_by_ios_predicate(element_location), by_ios_predicate
            )
            fetch_and_click(BaseAppPage.click_on_element_by_image(element_location), by_image)

    @staticmethod
    def click_on_element_by_accessibility_id(element_location):
        BaseAppPage.wait_for_element(MBy.ACCESSIBILITY_ID, element_location, is_clickable=True)
        BaseAppPage.find_by_accessibility_id(element_location).click()

    @staticmethod
    def click_on_element_by_android_uiautomator(element_location):
        BaseAppPage.wait_for_element(MBy.ANDROID_UIAUTOMATOR, element_location, is_clickable=True)
        BaseAppPage.find_by_android_uiautomator(element_location).click()

    @staticmethod
    def click_on_element_by_android_viewtag(element_location):
        BaseAppPage.wait_for_element(MBy.ANDROID_VIEWTAG, element_location, is_clickable=True)
        BaseAppPage.find_by_android_viewtag(element_location).click()

    @staticmethod
    def click_on_element_by_xpath(element_location):
        BaseAppPage.wait_for_element(MBy.XPATH, element_location)
        BaseAppPage.find_by_xpath(element_location).click()

    @staticmethod
    def click_on_element_by_css_selector(element_location):
        BaseAppPage.wait_for_element(MBy.CSS_SELECTOR, element_location)
        BaseAppPage.find_by_css_selector(element_location).click()

    @staticmethod
    def click_on_element_by_class_name(element_location):
        BaseAppPage.wait_for_element(MBy.CLASS_NAME, element_location)
        BaseAppPage.find_by_class_name(element_location).click()

    @staticmethod
    def click_on_element_by_custom(element_location):
        BaseAppPage.wait_for_element(MBy.CUSTOM, element_location)
        BaseAppPage.find_by_custom(element_location).click()

    @staticmethod
    def click_on_element_by_id(element_location):
        BaseAppPage.wait_for_element(MBy.ID, element_location)
        BaseAppPage.find_by_id(element_location).click()

    @staticmethod
    def click_on_element_by_image(element_location):
        BaseAppPage.wait_for_element(MBy.IMAGE, element_location)
        BaseAppPage.find_by_image(element_location).click()

    @staticmethod
    def click_on_element_by_ios_class_chain(element_location):
        BaseAppPage.wait_for_element(MBy.IOS_CLASS_CHAIN, element_location)
        BaseAppPage.find_by_ios_class_chain(element_location).click()

    @staticmethod
    def click_on_element_by_ios_predicate(element_location):
        BaseAppPage.wait_for_element(MBy.IOS_PREDICATE, element_location)
        BaseAppPage.find_by_ios_predicate(element_location).click()

    @staticmethod
    def click_on_element_by_ios_uiautomation(element_location):
        BaseAppPage.wait_for_element(MBy.IOS_UIAUTOMATION, element_location)
        BaseAppPage.find_by_ios_uiautomation(element_location).click()

    @staticmethod
    def click_on_element_by_name(element_location):
        BaseAppPage.wait_for_element(MBy.NAME, element_location)
        BaseAppPage.find_by_name(element_location).click()

    @staticmethod
    def click_on_element_by_tag_name(element_location):
        BaseAppPage.wait_for_element(MBy.TAG_NAME, element_location)
        BaseAppPage.find_by_tag_name(element_location).click()

    @staticmethod
    def click_on_list_of_elements(by_type, root_elements_location):
        element_list_ = BaseAppPage.get_elements_by(by_type, root_elements_location)
        for item in range(len(element_list_)):
            element_list_[item].click()

    @staticmethod
    def format_prices_to_number(by_type, element_location):
        items_found = BaseAppPage.get_elements_by(by_type, element_location)
        labels_found = []
        for item in items_found:
            price_fmt = String.convert_currency_to_number(value_to_format=item.text)
            labels_found.append(price_fmt)
        return labels_found

    @staticmethod
    def format_numbers_to_price(labels, by_type="", element_location="", symbol=""):
        items_found = (
            BaseAppPage.get_elements_by(by_type, element_location)
            if element_location != ""
            else labels
        )
        BaseAppPage.wait_for_element(by=by_type, location=element_location)
        for item in items_found:
            price = String.extract_number(item.text)
            price_fmt = String.convert_number_to_currency(value_to_format=price, currency=symbol)
            labels.append(price_fmt)
        return labels

    @staticmethod
    def tap(by_type="", element_location=""):
        element = BaseAppPage.find_by(by_type, element_location)
        action = TouchAction(WebDriver.use())
        action.tap(element).perform()

    @staticmethod
    def choose_random_value(values_list):
        list_size = len(values_list) - 1
        random_option = int(
            RandomData.generate_random_data(
                length=3, start_threshold=0, end_threshold=list_size, step=1, only_numbers=True
            )
        )
        return values_list[random_option]

    @staticmethod
    def _choose_random_element(by_type, element_location):
        BaseAppPage.wait_for_element(by_type, element_location)
        options_ = BaseAppPage.list_element_strings(by_type, element_location)
        total_options = len(options_) - 1
        single_item_max = 1
        threshold = 0 if total_options < single_item_max else single_item_max
        random_value = (
            threshold
            if total_options <= single_item_max
            else RandomData.generate_random_data(
                length=4, start_threshold=1, end_threshold=total_options, only_numbers=True
            )
        )
        random_option = options_[int(random_value)]
        print(f"   └> Random option chosen: {random_option}")
        return random_option

    @staticmethod
    def find_a_limit_value_in_list(by_type, element_location, max_value=False):
        """Find Max or Min value in list of elements
        Args:
            by_type (By): Use MBy that defines the drop_locator
            element_location (str): Locator string from an element (can be an XPATH, ID, CSS_SELECTOR, etc.)
            max_value (bool, optional): Set it to True if you need only a max value into a list found. Defaults to False.
        Returns:
            [int]: Value found according parameter expected: if max or min number into the list
        """
        BaseAppPage.wait_for_element(by_type, element_location)
        items_found = BaseAppPage.find_elements_by(by_type, element_location)
        labels_found = [float(String.extract_decimal(item.text)[0]) for item in items_found]
        return max(labels_found) if max_value else min(labels_found)

    @staticmethod
    def list_element_strings(by_type, element_location, options_location=""):
        options_locator = (by_type, element_location + options_location)
        BaseAppPage.wait_for_element(*options_locator)
        items_found = BaseAppPage.find_elements_by(*options_locator)
        labels_found = [item.text for item in items_found]
        if BaseAppPage.wait_for_element(*options_locator, is_presented=True):
            pass
        return labels_found[0].split("\n") if len(labels_found) == 1 else labels_found

    @staticmethod
    def select_dropdown_item(
        str_option,
        str_autocomplete="",
        root_by_type=MBy.XPATH,
        root_selector="",
        xpath_for_root_option="",
        xpath_with_a_option_set="",
        is_combobox=False,
        is_visible=False,
    ):
        """
        Select a dropdown item or find an option in an autocomplete input text filter.

        Args:
            str_option (str): The value used to be selected in the component
            str_autocomplete (str, optional): Text to be used in a search field with autocomplete function. Defaults to "".
            root_by_type (By.[TYPE], optional): A type for the "root_selector" argument. It can be a ID, XPATH or CSS_SELECTOR. Defaults to By.XPATH.
            root_selector (str, optional): A XPATH or CSS_SELECTOR to locate the root of a dropdown component. Defaults to "".
            xpath_for_root_option (str, optional): Generic selector to locate the root of elements presented in a visible dropdown list. Defaults to "".
            xpath_with_a_option_set (str, optional): Selector to a specific item presented in a visible dropdown list. Defaults to "".
            is_combobox (bool, optional): If you are considering the dropdown selection as a simple combobox. Defaults to False.
            is_visible (bool, optional): If you really needs the element visible at the page.
        """
        if is_combobox:
            BaseAppPage._combobox(str_option, root_by_type, root_selector)
        else:
            BaseAppPage._dynamic_dropdown(
                str_option,
                str_autocomplete,
                root_by_type,
                root_selector,
                xpath_for_root_option,
                xpath_with_a_option_set,
                is_component_visible=is_visible,
            )

    @staticmethod
    def _dynamic_dropdown(
        str_option,
        str_autocomplete,
        root_by_type,
        root_selector,
        xpath_for_root_option,
        xpath_with_a_option_set,
        is_component_visible,
    ):
        if BaseAppPage.is_not_empty_value(str_option):
            if str_autocomplete != "":
                BaseAppPage.type_text(
                    str_autocomplete,
                    root_by_type,
                    root_selector,
                    is_clickable=True,
                )
            else:
                BaseAppPage.click_on(root_by_type, root_selector, is_visible=is_component_visible)
            dropdown_item_value = (
                BaseAppPage._choose_random_element(MBy.XPATH, xpath_for_root_option)
                if str_option == "" and xpath_with_a_option_set == ""
                else str_option
            )
            text_finder = BaseAppPage.chain_dynamic_xpath_functions(
                searchable_text=dropdown_item_value
            )
            has_all_symbol = (
                "//*"
                if BaseAppPage.wait_for_element(
                    MBy.XPATH,
                    f"{xpath_for_root_option}//*{text_finder}",
                    is_presented=True,
                )
                is True
                else ""
            )
            full_selector_item = (
                f"{xpath_for_root_option}{has_all_symbol}{text_finder}"
                if xpath_for_root_option != ""
                else xpath_with_a_option_set
            )
            print(f"   └> Dynamic option to selection:\n      {full_selector_item}")
            BaseAppPage.wait_for_element(MBy.XPATH, full_selector_item)
            BaseAppPage.click_on(MBy.XPATH, full_selector_item, is_visible=is_component_visible)

    @staticmethod
    def _combobox(option, by_type, element_location):
        if BaseAppPage.is_not_empty_value(option):
            BaseAppPage.wait_for_element(by_type, element_location, is_clickable=True)
            select = Select(BaseAppPage.get_element_by(by_type, element_location))
            try:
                select.select_by_value(option)
            except:
                if String.is_not_blank_or_null(option):
                    select.select_by_visible_text(option)
            print(f"   └> Option chosen: {option}")
