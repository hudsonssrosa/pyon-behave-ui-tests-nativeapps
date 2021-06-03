import os
import json
import requests
import socket
import subprocess

from behave import fixture
from factory.singleton_web_driver import WebDriver
from factory.handling.base_logging import BaseLogging as Log
from factory.handling.running_exception import RunningException as Rexc
from factory.base_context import BaseContext as Bctx
from selenium import webdriver
from appium import webdriver as appium_driver

from settings.environment_data_provider import EnvSettings as Conf
from factory.utils.OsUtil import OsUtil
from factory.utils.FileUtil import FileUtil
from factory.utils.DataEncryptedUtil import DataEncrypted as RandomData

import urllib3

urllib3.disable_warnings()


cap_config = lambda conf_condition: True if conf_condition == "true" else False
set_flag_in_cap = (
    lambda flag_context, config_var: flag_context if flag_context != "" else config_var
)


def log_web_driver_error(ex):
    Rexc.raise_exception_error(f"Error to execute the Web Driver. \nPrevious cause: ", ex)


def log_web_driver_in_instance(webdriver_name):
    Log.success(f"▶ {str(webdriver_name).upper()} is running...")


def provide_webdriver(context, browser_session, wd_name):
    try:
        browser_session.maximize_window()
        WebDriver.delete_cookies()
    except Exception:
        pass
    log_web_driver_in_instance(wd_name + f"- ID: {Bctx.random_data.get()}")
    WebDriver.set_driver(browser_session)
    context.web = WebDriver.use()
    WebDriver.set_driver(context.web)
    yield WebDriver


@fixture(name="browserstack")
def browserstack(context):
    build_number = os.environ.get("BUILD_NUMBER", f"{Bctx.random_data.get()}")
    bs_username = os.environ.get("BS_USERNAME", Conf.get_bs_user_key())
    bs_authkey = os.environ.get("BS_ACCESS_KEY", Conf.get_bs_access_key())
    bs_os = Bctx.flag_os.get()
    bs_mobile_os = Bctx.flag_os.get()
    bs_mobile_os_version = Bctx.flag_os_version.get()
    bs_mobile_device = Bctx.flag_device_name.get()
    bs_mobile_orientation = Bctx.flag_orientation.get()
    caps = {
        "name": set_test_build_description(build_number),
        "project": "PYON-UI-TESTS-FOR-NATIVE-APPS",
        "build": set_project_build_description(build_number),
        "deviceName": bs_mobile_device,
        "device": bs_mobile_device,
        "platformName": bs_mobile_os,
        "os_version": bs_mobile_os_version,
        "deviceOrientation": bs_mobile_orientation,
        "app": os.environ["MOB_APP_ID"],
        "browserstack.video": Conf.get_bs_record_video(),
        "browserstack.local": "false",
        "browserstack.seleniumLogs": "true",
        "browserstack.appiumLogs": "false",
        "browserstack.networkLogs": "false",
        "realMobile": "true",
    }
    app_path = (
        str(os.path.abspath(Bctx.flag_mobile_app_path.get()))
        .replace("\\", os.sep)
        .replace("//", os.sep)
    )
    Log.info(app_path)
    result = os.popen(
        f'curl -u "{bs_username}:{bs_authkey}" -X POST "https://api-cloud.browserstack.com/app-automate/upload" -F "file=@{app_path}"'
    ).read()
    app_id = json.loads(result)
    OsUtil.set_env_var("MOB_APP_ID", str(app_id["app_url"]))
    web_rem = webdriver.Remote(
        command_executor=f"http://{bs_username}:{bs_authkey}@hub-cloud.browserstack.com/wd/hub",
        desired_capabilities=caps,
    )
    yield from provide_webdriver(
        context, web_rem, f"BROWSERSTACK: {Bctx.flag_mode.get()} - {bs_os}"
    )
    requests.put(
        f"https://{bs_username}:{bs_authkey}@api.browserstack.com/automate/sessions/<session-id>.json",
        data={"status": "passed", "reason": ""},
    )


@fixture(name="local_device")
def local_appium(context):
    localhost_ip = Conf.get_appium_host_ip()
    appium_port = Conf.get_appium_host_port()
    mobile_os = Bctx.flag_os.get()
    is_ios = mobile_os == "iOS"
    is_android = mobile_os == "Android"
    andr_device_serial_list = find_serial_number_from_adb_device(is_android)
    mobile_os_version = Bctx.flag_os_version.get()
    mobile_orientation = Bctx.flag_orientation.get()
    mobile_language = Bctx.flag_language.get()
    mobile_locale = Bctx.flag_locale.get()
    locale_by_platform = str(mobile_locale)[-2:] if len(mobile_locale) > 2 else mobile_locale
    mobile_app_path = Bctx.flag_mobile_app_path.get()
    device_name = Bctx.flag_device_name.get()
    is_mobile_mode = Bctx.flag_mode.get() == "mobile"
    is_native_app_mode = Bctx.flag_mode.get() == "native_app"
    is_local_device = device_name == "local"

    mobile_device = (
        str(andr_device_serial_list).replace("List ", "").replace("\n", "")
        if is_local_device and is_android
        else device_name
    )
    default_automation_name_config = Conf.get_mobile_automation_name()
    mobile_automation_name = (
        "XCUITest" if is_ios else ("UiAutomator2" if is_android else default_automation_name_config)
    )
    url = f"http://{localhost_ip}:{appium_port}/wd/hub"

    try:
        if is_mobile_mode or is_native_app_mode:
            caps = {
                "platformName": mobile_os,
                "platformVersion": mobile_os_version,
                "deviceName": mobile_device,
                "app": mobile_app_path,
                "deviceOrientation": mobile_orientation,
                "automationName": mobile_automation_name,
                "language": mobile_language,
                "locale": locale_by_platform,
                "allowTestPackages": "true",
                "clearSystemFiles": "true",
                "connectHardwareKeyboard": "true",
                "fullReset": "true",
                "newCommandTimeout": "120",
                "noReset": "false",
            }
            if is_ios:
                caps["autoAcceptAlerts"] = "false"
                caps["autoDismissAlerts"] = "false"
                caps["keepKeyChains"] = "true"
                caps["waitForAppScript"] = "true"
            if is_android:
                caps["autoGrantPermissions"] = "true"
            if mobile_automation_name == "XCUITest":
                caps["useNewWDA"] = "true"
                caps["wdaLocalPort"] = "9000"
                caps["wdaConnectionTimeout"] = "60000"
                caps["resetOnSessionStartOnly"] = "true"
                caps["agentPath"] = Conf.get_xcode_webdriveragent_path()
                caps["bootstrapPath"] = Conf.get_xcode_webdriveragent_bootstrap_path()

            app_rem = appium_driver.Remote(url, desired_capabilities=caps, direct_connection=False)
            yield from provide_webdriver(context, app_rem, "LOCAL DEVICE: " + mobile_device)
    except Exception as ex:
        Rexc.raise_exception_error(
            "Appium Server is not started or is not properly configured.", ex
        )


@fixture(name="remote_device")
def remote_appium(context):
    localhost_ip = Conf.get_appium_host_ip()
    appium_port = Conf.get_appium_host_port()
    wda_port = str(
        RandomData.generate_random_data(
            length=4, start_threshold=8100, end_threshold=8300, step=1, only_numbers=True
        )
    )
    mobile_os = Bctx.flag_os.get()
    is_ios = mobile_os == "iOS"
    is_android = mobile_os == "Android"
    andr_device_serial_list = find_serial_number_from_adb_device(is_android)
    mobile_os_version = Bctx.flag_os_version.get()
    mobile_orientation = Bctx.flag_orientation.get()
    mobile_language = Bctx.flag_language.get()
    mobile_locale = Bctx.flag_locale.get()
    locale_by_platform = str(mobile_locale)[-2:] if len(mobile_locale) > 2 else mobile_locale
    device_name = Bctx.flag_device_name.get()
    mobile_app_path = Bctx.flag_mobile_app_path.get()
    is_mobile_mode = Bctx.flag_mode.get() == "mobile"
    is_native_app_mode = Bctx.flag_mode.get() == "native_app"

    mobile_device = (
        str(andr_device_serial_list).replace("List ", "").replace("\n", "")
        if is_android
        else device_name
    )
    default_automation_name_config = Conf.get_mobile_automation_name()
    mobile_automation_name = (
        "XCUITest" if is_ios else ("UiAutomator2" if is_android else default_automation_name_config)
    )

    wda_xcodeproj = "WebDriverAgent.xcodeproj"
    wda_root_dirs = ["usr", "local", "lib", "node_modules", "appium", "node_modules"]
    wda_root = str(os.sep).join(wda_root_dirs[:])
    wda_specific_dirs = ["appium-webdriveragent", "appium-xcuitest-driver", "appium-ios-simulator"]
    default_wda_path = f"{os.sep}{wda_root}{os.sep}appium-webdriveragent{os.sep}{wda_xcodeproj}"
    for wda_lastfolder in wda_specific_dirs:
        full_wda_path = f"{os.sep}{wda_root}{os.sep}{wda_lastfolder}{os.sep}{wda_xcodeproj}"
        if os.path.exists(full_wda_path):
            default_wda_path = full_wda_path
            os.system(
                f"mkdir -p {os.sep}{wda_root}{os.sep}{wda_lastfolder}{os.sep}Resources{os.sep}WebDriverAgent.bundle"
            )
            os.system(
                f"{os.sep}{wda_root}{os.sep}{wda_lastfolder}{os.sep}Scripts{os.sep}bootstrap.sh -d"
            )
            break
        else:
            default_wda_path = f"{wda_root}{os.sep}{wda_xcodeproj}"

    bootstrap_wda_path = FileUtil.remove_last_element_from_path(default_wda_path)
    os.system(f"echo '-- DRIVER PATH BOOTED: {bootstrap_wda_path} --'")
    os.system(f"ls {bootstrap_wda_path}")
    os.system("echo '--------------------'")

    os.system(f"echo '-- APP FROM BUILD AVAILABLE IN: {mobile_app_path} --'")
    os.system(f"ls {mobile_app_path}")
    os.system("echo '--------------------'")

    url = f"http://{localhost_ip}:{appium_port}/wd/hub"

    try:
        if is_mobile_mode or is_native_app_mode:
            caps = {
                "platformName": mobile_os,
                "platformVersion": mobile_os_version,
                "deviceName": mobile_device,
                "app": mobile_app_path,
                "deviceOrientation": mobile_orientation,
                "automationName": mobile_automation_name,
                "language": mobile_language,
                "locale": locale_by_platform,
                "allowTestPackages": "true",
                "connectHardwareKeyboard": "true",
                "newCommandTimeout": "130",
                "noReset": "false",
                "fullReset": "true",
                "clearSystemFiles": "true",
            }
            if is_ios:
                caps["autoAcceptAlerts"] = "false"
                caps["autoDismissAlerts"] = "false"
                caps["keepKeyChains"] = "true"
                caps["waitForAppScript"] = "true"
                caps["showXcodeLog"] = "true"
                caps["wdaLocalPort"] = wda_port
                caps["wdaConnectionTimeout"] = "60000"
                caps["shouldUseSingletonTestManager"] = "false"
            if is_android:
                caps["autoGrantPermissions"] = "true"
            # KEEP THESE CAPABILITIES COMMENTED IF RUN INTO BITRISE
            # if mobile_automation_name == "XCUITest":
            #     caps["useNewWDA"] = "true"

            #     caps["resetOnSessionStartOnly"] = "true"
            #     caps["webDriverAgentUrl"] = f"http://localhost:{wda_port}"
            #     caps["agentPath"] = default_wda_path
            #     caps["bootstrapPath"] = bootstrap_wda_path

            app_rem = appium_driver.Remote(
                url, desired_capabilities=caps, proxy=None, direct_connection=False
            )
            yield from provide_webdriver(
                context, app_rem, "REMOTE EXECUTION - DEVICE: " + mobile_device
            )
    except Exception as ex:
        Rexc.raise_exception_error(
            "Appium Server is not started or is not properly configured.", ex
        )


def find_serial_number_from_adb_device(is_android):
    return (
        subprocess.Popen(
            "echo `adb devices | awk '{print $1}'`", shell=True, stdout=subprocess.PIPE
        )
        .communicate()[0]
        .decode("utf-8")
        if is_android
        else ""
    )


def set_test_build_description(build_number):
    environment = str(Bctx.flag_environment.get()).upper()
    scenario = Bctx.flag_scenario.get()
    tags_fmt = "Tag: #" + Bctx.cur_tag.get() if scenario is not None or scenario != "" else ""
    return f"[{build_number}] | {environment} | {tags_fmt} {scenario}"


def set_project_build_description(build_number):
    environment = str(Bctx.flag_environment.get()).upper()
    hostname = "-"
    try:
        hostname = socket.gethostname()
    except:
        hostname = "Undefined"
    tags = (
        "Tags: #"
        + str(
            str(Bctx.flag_tags.get()).replace("--tags=", "").replace("-", " ").replace(",", "  #")
        )
        .title()
        .strip()
    )
    return f"BUILD-[{build_number}]-PyonUIT | {environment} | {tags} | Server-{hostname}"


fixture_registry = {
    "browserstack": browserstack,
    "local_device": local_appium,
    "remote_device": remote_appium,
}
