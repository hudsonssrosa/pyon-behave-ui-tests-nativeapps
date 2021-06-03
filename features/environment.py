from behave import use_fixture
from features import fixtures
from factory.singleton_web_driver import WebDriver
from factory.handling.base_logging import BaseLogging as Log
from factory.base_context import BaseContext as Bctx
from factory.handling.running_exception import RunningException as Rexc
from settings.environment_data_provider import EnvSettings as Conf
from settings.secrets_data_provider import SecretsSettings as SecFile
from factory.utils.DataEncryptedUtil import DataEncrypted as RandData

import os
import sys
import urllib3
import traceback

urllib3.disable_warnings()

EXCLUDE_TAG = Bctx.flag_exclude.get()
SKIP_TAG = EXCLUDE_TAG if EXCLUDE_TAG is not None or EXCLUDE_TAG != "None" else "skip"
message_skipped_tags = f"    \n ctx SKIPPED WITH TAG: @{SKIP_TAG}"


def before_all(context):
    app_env = {
        "dev": Conf.get_url_app_dev(),
        "staging": Conf.get_url_app_staging(),
        "production": Conf.get_url_app_prod(),
    }
    admin_env = {
        "dev": Conf.get_admin_url_dev(),
        "staging": Conf.get_admin_url_staging(),
        "production": Conf.get_admin_url_prod(),
    }
    context.config.setup_logging()
    context.url = app_env[Bctx.flag_environment.get()]
    context.admin_url = admin_env[Bctx.flag_environment.get()]
    context.email_url = Conf.get_email_url()
    Bctx.random_data.set(RandData.generate_random_data(length=7))
    Log.info(f"Hash available for test scope: {Bctx.random_data.get()}")
    Bctx.configcat_sdk_key_ff_dev.set(SecFile.get_secret_configcat_sdk_key_ff_dev())
    Bctx.configcat_sdk_key_ff_staging.set(SecFile.get_secret_configcat_sdk_key_ff_staging())
    Bctx.configcat_sdk_key_ff_production.set(SecFile.get_secret_configcat_sdk_key_ff_production())
    Bctx.app_url.set(context.url)
    Bctx.admin_url.set(context.admin_url)
    Bctx.email_url.set(context.email_url)
    Log.info(f"ConfigCat SDK Keys are ready!")


def before_feature(context, feature):
    Log.gherkin_feature_info(feature)
    if SKIP_TAG in feature.tags:
        feature.skip(f"Marked with @{SKIP_TAG}")
        Log.warning(message_skipped_tags.replace("ctx", "FEATURE"))
        return


def after_feature(context, feature):
    print("\n")


def before_scenario(context, scenario):
    reset_xcode_simulator()
    scn_tags = f"---> TAG(s): @{scenario.effective_tags[len(scenario.effective_tags) - 1]}\n"
    Log.gherkin_scenario_info(f"{scenario} {scn_tags}")
    if SKIP_TAG in scenario.effective_tags:
        scenario.skip(f"Marked with @{SKIP_TAG}")
        Log.warning(message_skipped_tags.replace("ctx", "SCENARIO"))
        return
    Bctx.flag_scenario.set(f"{scenario}")
    target_context = Bctx.flag_target.get()
    platform_execution = (
        lambda flag_cmd, fixture_def: use_fixture(fixture_def, context) if flag_cmd else None
    )
    try:
        platform_execution(target_context == "remote_emulation", fixtures.remote_appium)
        platform_execution(target_context == "local_emulation", fixtures.local_appium)
        platform_execution(target_context == "real_device", fixtures.local_appium)
        platform_execution(target_context == "bs", fixtures.browserstack)
    except Exception as ex:
        Rexc.raise_exception_error(f"RAISING ERROR.\n   Previous cause: ", ex)


def after_scenario(context, scenario):
    WebDriver.quit_webdriver()
    shutdown_xcode_simulator()


def before_step(context, step):
    Log.gherkin_step_info(step)


def after_step(context, step):
    if step.status == "passed":
        Log.status_passed()
    if step.status == "failed":
        txt_tb = "".join(traceback.format_tb(step.exc_traceback))
        Log.status_failed(stacktrace=txt_tb)
        take_screenshot_when_is_failed(context)


def before_tag(context, tag):
    Bctx.cur_tag.set(tag)


def take_screenshot_when_is_failed(context):
    try:
        WebDriver.take_screenshot("Failed")
    except:
        pass


def reset_xcode_simulator():
    if Conf.get_mobile_automation_name() == "XCUITest":
        os.system("xcrun simctl erase all")


def shutdown_xcode_simulator():
    if Conf.get_mobile_automation_name() == "XCUITest":
        os.system("xcrun simctl shutdown all")
