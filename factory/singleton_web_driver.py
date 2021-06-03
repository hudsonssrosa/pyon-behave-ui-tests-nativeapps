import io
import os
import json
import requests
import allure
import pickle
import time

from allure_commons.types import AttachmentType
from PyPDF2 import PdfFileReader
from factory.base_context import BaseContext as Bctx
from factory.handling.base_logging import BaseLogging as Log
from factory.handling.running_exception import RunningException as Rexc
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from factory.utils.DataEncryptedUtil import DataEncrypted as RandData


class WebDriver(object):

    TIMEOUT_SECS = 30
    driver = None

    def __init__(cls, browser_session):
        cls.log = Log
        cls._web_driver_wait = WebDriverWait(browser_session, WebDriver.TIMEOUT_SECS)
        cls.driver = browser_session

    def __str__(cls):
        return cls.driver

    def set_driver(browser):
        WebDriver.driver = browser
        return WebDriver.driver

    @staticmethod
    def use():
        try:
            return WebDriver.driver
        except Exception as ex:
            Rexc.raise_exception_error(f"Error found using this web driver instance!", ex)

    @staticmethod
    def log_action(element_location, action_name=""):
        loc_element_str = (
            [element_location][0] if len([element_location]) < 2 else [element_location][1]
        )
        Log.info(f"Selenium action: {str(action_name).upper()} --> {str(loc_element_str)}")

    # BASIC DRIVER HANDLING

    @staticmethod
    def get_info_from_cookies(key):
        cookies = None
        browser_cookies = WebDriver.use().get_cookies()
        pickle.dump(browser_cookies, open("cookies.pkl", "wb"))
        with open("cookies.pkl", "rb") as cookie_file:
            cookies = pickle.load(cookie_file)
        return json.loads(json.dumps(cookies, sort_keys=True, indent=4))[0][str(key)]

    @staticmethod
    def delete_cookies():
        Log.info("Deleting browser cookies...")
        WebDriver.use().delete_all_cookies()

    @staticmethod
    def close_webdriver():
        WebDriver.use().close()

    @staticmethod
    def quit_webdriver():
        try:
            if WebDriver.use() is not None:
                WebDriver.use().quit()
                Log.info("⏹ Web Driver stopped!\n")
        except Exception:
            Log.warning("∅ Web Driver not started!\n")
            pass

    @staticmethod
    def open_window(_url):
        WebDriver.use().get(_url)
        WebDriver.get_browser_console_log(_url)

    @staticmethod
    def open(_url):
        response = requests.get(_url, verify=False, params="", timeout=15)
        try:
            time.sleep(0.5)
            WebDriver.execute_javascript(f'window.open("{_url}","_self")')
            Log.info(f"PAGE OPEN: {WebDriver.current_url()}")
            WebDriver.get_browser_console_log(_url)
            assert response.status_code != 500
            assert response.status_code != 503
        except AssertionError as ae:
            Rexc.raise_assertion_error(
                f"Server is unavailable: STATUS {response.status_code} for {_url}", ae
            )

    @staticmethod
    def open_new_tab(_url, number=0):
        if int(number) == 0:
            WebDriver.open(_url)
        else:
            WebDriver.execute_javascript("window.open('');")
            WebDriver.switch_to_tab(number)
            WebDriver.open(_url)

    @staticmethod
    def current_url():
        return WebDriver.use().current_url

    @staticmethod
    def maximize_window():
        WebDriver.use().maximize_window()

    @staticmethod
    def refresh_page():
        WebDriver.use().refresh()

    @staticmethod
    def back_page():
        WebDriver.use().back()

    @staticmethod
    def forward_page():
        WebDriver.use().forward()

    @staticmethod
    def get_page_to_load():
        WebDriver.use().set_page_load_timeout(WebDriver.TIMEOUT_SECS)

    @staticmethod
    def try_endpoint(_url):
        if Bctx.flag_environment.get() != "production":
            response = None
            try:
                response = requests.head(_url)
                assert response.status_code != 500
                assert response.status_code != 503
            except AssertionError as ae:
                Rexc.raise_assertion_error(
                    f"Service is down or does not exist: STATUS {response.status_code} for {_url}",
                    ae,
                )

    @staticmethod
    def current_window():
        return WebDriver.use().current_window_handle

    @staticmethod
    def switch_to_tab(number=0, last_tab=False):
        existing_tabs = WebDriver.use().window_handles
        if len(existing_tabs) > 1 and last_tab is False:
            WebDriver.use().switch_to.window(WebDriver.use().window_handles[int(number)])
            try:
                WebDriver.wait_for_element(by=By.CSS_SELECTOR, location="html")
            except:
                pass
        elif last_tab:
            WebDriver.use().switch_to.window(WebDriver.use().window_handles[len(existing_tabs) - 1])
        else:
            WebDriver.use().switch_to.window(WebDriver.use().window_handles[0])
        WebDriver.get_browser_console_log("")
        return WebDriver.use().current_window_handle

    @staticmethod
    def close_tab(number):
        WebDriver.use().switch_to.window(WebDriver.use().window_handles[int(number)])
        WebDriver.use().close()

    @staticmethod
    def close_all_tabs():
        existing_tabs = WebDriver.use().window_handles
        tabs = WebDriver.use().window_handles
        for i in range(len(existing_tabs)):
            WebDriver.close_tab(i)

    @staticmethod
    def close_all_tabs_but_one(number=0):
        tabs = WebDriver.use().window_handles
        for handle in tabs:
            if tabs[number] == handle:
                pass
            else:
                WebDriver.close_tab(number=1)
        WebDriver.switch_to_tab(number)

    # SCREENSHOT

    @staticmethod
    def take_screenshot(file_name):
        screenshot_path = Bctx.screenshot_path.get()
        scr_file_name = RandData.generate_random_data(length=10)
        scr_path = f"{screenshot_path}{os.sep}{file_name}_{scr_file_name}.png"
        WebDriver.use().save_screenshot(scr_path)
        allure.attach(
            WebDriver.use().get_screenshot_as_png(),
            f"{file_name}",
            attachment_type=AttachmentType.PNG,
        )
        Log.warning(f"Screenshot taken! --> {scr_path}")

    # DATA HANDLING

    @staticmethod
    def generate_random_string_data(input_text):
        """
        Use this method to get a hash string already generate in the context by the environment class.
        The context that carries this random string can be called separately by 'BaseContext.random_data.get()'

        Args:
            input_text (str): If the string passed in the args contains some '_RANDOM_DATA_', this will be replaced with a random hash string.
            Very useful to tests that needs to create diferent users or random data for any circumstance.

        Returns:
            str: If you have some text like 'john_doe__RANDOM_DATA_', then this will be placed to 'john_doe_klw37v0', for example.
        """
        if str(input_text).__contains__("_RANDOM_DATA_"):
            input_text_ = str(input_text).replace("_RANDOM_DATA_", Bctx.random_data.get())
            print(f"   └> Replaced string with random data: {input_text_}")
        else:
            input_text_ = input_text
        return input_text_

    @staticmethod
    def bind_secret_data(input_secret_tag, env_variable):
        try:
            if str(input_secret_tag).__contains__("_SECRET_DATA_"):
                return str(input_secret_tag).replace("_SECRET_DATA_", env_variable)
            else:
                return input_secret_tag
        except:
            return input_secret_tag

    @staticmethod
    def extract_pdf_content(file_path, page_number=1):
        req = requests.get(file_path)
        file_ = io.BytesIO(req.content)
        reader = PdfFileReader(file_)
        contents = reader.getPage(int(page_number) - 1).extractText().split("\n")
        return contents

    @staticmethod
    def prepare_locator(value, selector):
        str_marker = "<PLACE_TEXT>"
        return str(selector).replace(str_marker, str(value)) if str_marker in selector else selector

    @staticmethod
    def is_not_empty_value(value_to_check):
        return "-.-" not in str(value_to_check)

    @staticmethod
    def get_browser_console_log(url=""):
        try:
            for entry in WebDriver.use().get_log("browser"):
                message_title = f"     JAVASCRIPT ISSUES DETECTED IN: {url}"
                if "SEVERE" in json.loads(json.dumps(entry))["level"]:
                    Log.error(message_title)
                    Log.error(" " + str(entry))
                else:
                    Log.warning(message_title)
                    Log.warning(" " + str(entry))
        except:
            pass

    # ELEMENTS HANDLING

    @staticmethod
    def execute_javascript(script, *args):
        return WebDriver.use().execute_script(script, *args)

    @staticmethod
    def switch_nested_frame(by_type, frame_location):
        WebDriver.switch_to_default_content()
        WebDriver.wait_for_element(by=by_type, location=frame_location)
        frame_element = WebDriver.find_by(by_type, frame_location)
        WebDriver.use().switch_to.frame(frame_element)

    @staticmethod
    def switch_to_default_content():
        try:
            try:
                WebDriver.use().switch_to.default_content()
            except:
                WebDriver.execute_javascript("return self.name")
        except Exception as re:
            Rexc.raise_assertion_error(f"It was not possible to locate a default content!", re)

    def chain_dynamic_xpath_functions(searchable_text):
        """Xpath to find a text considering Starts-with(), Contains(text) or Contains(text) with insensitive case

        Args:
            searchable_text (str): Should it be informed the text to be searched in a DOM tree.

        Returns:
            str: XPath fragment with functions to find text dinamically is returned.
        """
        upper_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        lower_chars = upper_chars.lower()
        find_lower_case = f'contains(translate(.,"{upper_chars}","{lower_chars}"),"{str(searchable_text).lower()}")'
        find_upper_case = (
            f'contains(translate(.,"{lower_chars}","{upper_chars}"),"{searchable_text}")'
        )
        xpath_f_case_insentitive = f"{find_lower_case} or {find_upper_case}"
        xpath_f_contains_text = f'contains(text(),"{searchable_text}")'
        xpath_f_starts_with = f'starts-with(text(),"{searchable_text}")'
        return f"[{xpath_f_starts_with} or {xpath_f_contains_text} or {xpath_f_case_insentitive}]"

    @staticmethod
    def find_by(by_type, element_location):
        action_chains = ActionChains(WebDriver.use())
        try:
            element = WebDriver.use().find_element(by_type, element_location)
            action_chains.move_to_element(element)
            return element
        except Exception as re:
            Rexc.raise_assertion_error(f"Element '{element_location}' was not found!", re)

    @staticmethod
    def find_elements_by(by_type, element_location):
        try:
            return WebDriver.use().find_elements(by_type, element_location)
        except Exception as re:
            Rexc.raise_assertion_error(f"Elements '{element_location}' were not found!", re)

    @staticmethod
    def find_by_xpath(selector):
        try:
            return WebDriver.use().find_element_by_xpath(xpath=selector)
        except Exception as re:
            Rexc.raise_assertion_error(f"Element '{selector}' was not found!", re)

    @staticmethod
    def find_by_accessibility_id(selector):
        try:
            return WebDriver.use().find_element_by_accessibility_id(accessibility_id=selector)
        except Exception as re:
            Rexc.raise_assertion_error(f"Element '{selector}' was not found!", re)

    @staticmethod
    def find_by_android_viewtag(selector):
        try:
            return WebDriver.use().find_element_by_android_viewtag(tag=selector)
        except Exception as re:
            Rexc.raise_assertion_error(f"Element '{selector}' was not found!", re)

    @staticmethod
    def find_by_android_uiautomator(selector):
        try:
            return WebDriver.use().find_element_by_android_uiautomator(
                uia_string="new UiSelector()." + selector
            )
        except Exception as re:
            Rexc.raise_assertion_error(f"Element '{selector}' was not found!", re)

    @staticmethod
    def find_by_class_name(selector):
        try:
            return WebDriver.use().find_element_by_class_name(name=selector)
        except Exception as re:
            Rexc.raise_assertion_error(f"Element '{selector}' was not found!", re)

    @staticmethod
    def find_by_css_selector(selector):
        try:
            return WebDriver.use().find_element_by_css_selector(css_selector=selector)
        except Exception as re:
            Rexc.raise_assertion_error(f"Element '{selector}' was not found!", re)

    @staticmethod
    def find_by_custom(selector):
        try:
            return WebDriver.use().find_element_by_custom(selector=selector)
        except Exception as re:
            Rexc.raise_assertion_error(f"Element '{selector}' was not found!", re)

    @staticmethod
    def find_by_id(selector):
        try:
            return WebDriver.use().find_element_by_id(id_=selector)
        except Exception as re:
            Rexc.raise_assertion_error(f"Element '{selector}' was not found!", re)

    @staticmethod
    def find_by_image(selector):
        try:
            return WebDriver.use().find_element_by_image(img_path=selector)
        except Exception as re:
            Rexc.raise_assertion_error(f"Element '{selector}' was not found!", re)

    @staticmethod
    def find_by_ios_class_chain(selector):
        try:
            return WebDriver.use().find_element_by_ios_class_chain(class_chain_string=selector)
        except Exception as re:
            Rexc.raise_assertion_error(f"Element '{selector}' was not found!", re)

    @staticmethod
    def find_by_ios_predicate(selector):
        try:
            return WebDriver.use().find_element_by_ios_predicate(predicate_string=selector)
        except Exception as re:
            Rexc.raise_assertion_error(f"Element '{selector}' was not found!", re)

    @staticmethod
    def find_by_ios_uiautomation(selector):
        try:
            return WebDriver.use().find_element_by_ios_uiautomation(uia_string=selector)
        except Exception as re:
            Rexc.raise_assertion_error(f"Element '{selector}' was not found!", re)

    @staticmethod
    def find_by_name(selector):
        try:
            return WebDriver.use().find_element_by_name(name=selector)
        except Exception as re:
            Rexc.raise_assertion_error(f"Element '{selector}' was not found!", re)

    @staticmethod
    def find_by_tag_name(selector):
        try:
            return WebDriver.use().find_element_by_tag_name(name=selector)
        except Exception as re:
            Rexc.raise_assertion_error(f"Element '{selector}' was not found!", re)

    @staticmethod
    def is_selected(by_type, element_location):
        return WebDriver.use().find_element(by_type, element_location).is_selected()

    @staticmethod
    def get_element_by(by_type, element_location):
        WebDriver.wait_for_element(by=by_type, location=element_location)
        return WebDriver.find_by(by_type, element_location)

    @staticmethod
    def get_elements_by(by_type, element_location):
        WebDriver.wait_for_element(by=by_type, location=element_location)
        return WebDriver.find_elements_by(by_type, element_location)

    @staticmethod
    def wait_for_element(
        by=By.XPATH,
        location="//*",
        with_text="",
        title="",
        is_visible=False,
        is_not_visible=False,
        is_clickable=False,
        is_selected=False,
        is_frame=False,
        is_alert=False,
        is_presented=False,
        typing_secs=float(0),
        handle_timeout=1,
    ):
        bundle_wait = []
        location = str(location)
        browser_timeout = (
            (WebDriver.TIMEOUT_SECS if WebDriver.TIMEOUT_SECS is not None else 5)
            if handle_timeout == 0
            else handle_timeout
        )
        try:
            if is_presented:
                WebDriver.add_slowness(by, location, slowness_freq=0.3)
                return len(WebDriver.find_elements_by(by, location)) > 0
            else:
                ec_dicts = {
                    1: {
                        "wait": ec.visibility_of_element_located((by, location)),
                        "state": is_visible,
                    },
                    2: {"wait": ec.element_to_be_clickable((by, location)), "state": is_clickable},
                    3: {
                        "wait": ec.invisibility_of_element_located((by, location)),
                        "state": is_not_visible,
                    },
                    4: {
                        "wait": ec.frame_to_be_available_and_switch_to_it((by, location)),
                        "state": is_frame,
                    },
                    5: {"wait": ec.alert_is_present(), "state": is_alert},
                    6: {"wait": ec.title_contains(title), "state": title != ""},
                    7: {
                        "wait": ec.text_to_be_present_in_element((by, location), with_text),
                        "state": with_text != "",
                    },
                    8: {"wait": ec.element_to_be_selected((by, location)), "state": is_selected},
                    9: {
                        "wait": ec.text_to_be_present_in_element_value((by, location), with_text),
                        "state": with_text != ""
                        and WebDriver.find_by(by, location).get_attribute(str("value")),
                    },
                }
                bundle_wait = [
                    lambda ec_item: WebDriverWait(WebDriver.use(), browser_timeout).until(
                        ec_item["wait"]
                    )
                    for wait_enum, ec_item in ec_dicts.items()
                    if ec_item["state"]
                ]
                WebDriver.retry_element(by, location, browser_timeout, typing_secs)
                return bundle_wait
        except (TimeoutError, Exception) as te:
            Rexc.raise_assertion_error(
                f"Element not found. Expected conditions: {len(bundle_wait)}\nMax retries exceeded --> {str(location)}",
                te,
            )

    @staticmethod
    def retry_element(by, location, browser_timeout, typing_secs):
        try:
            initial_timeout = 5
            type_slow_secs = (
                WebDriver.add_slowness(by, location, slowness_freq=typing_secs)
                if typing_secs > 0
                else 0
            )
            WebDriverWait(WebDriver.use(), initial_timeout).until(
                ec.presence_of_element_located((by, location)),
                ignored_exceptions=StaleElementReferenceException,
            )
        except:
            WebDriverWait(WebDriver.use(), browser_timeout).until(
                ec.presence_of_element_located((by, location))
            )

    @staticmethod
    def add_slowness(by="", location="", timeout=0.0, slowness_freq=0.001):
        try:
            WebDriverWait(
                WebDriver.use(),
                timeout,
                poll_frequency=float(slowness_freq),
                ignored_exceptions=NoSuchElementException,
            ).until_not(ec.presence_of_element_located((by, location)))
        except:
            pass
