import argparse
from factory.base_context import BaseContext as Bctx
from factory.handling.base_logging import BaseLogging as Log
from settings.environment_data_provider import EnvSettings as Conf
from settings.collections.lang_locale_collection import LanguageLocationChoices as Lang
from settings.collections.devices_collection import DeviceChoices as Device


class Cli:
    @staticmethod
    def parse_external_args():
        parser = argparse.ArgumentParser(usage="%(prog)s [options]")
        parser.add_argument(
            "--environment",
            choices=["staging", "dev", "production"],
            help="==> Environment to execute the tests (default = staging). Find the app URLs in properties file",
            default="staging",
        )
        parser.add_argument(
            "--target",
            choices=["remote_emulation", "local_emulation", "bs", "real_device"],
            help="==> Platform to execute the mobile tests (default = local_emulation): BS - BrowserStack",
            default="local_emulation",
        )
        parser.add_argument(
            "--mode",
            choices=["native_app"],
            help="==> Execution mode according the mobile platform (default = native_app)",
            default="native_app",
        )
        parser.add_argument(
            "--os",
            choices=["iOS", "Android", ""],
            type=str,
            help="==> Mobile Operational System",
            default="iOS",
        )
        parser.add_argument(
            "--os_version",
            choices=[
                "14.5",
                "14.4",
                "14.3",
                "14.2",
                "14.1",
                "14.0",
                "13.0",
                "12.0",
                "11.0",
                "10.0",
                "9.0",
                "8.1",
                "8.0",
                "7.1",
                "7.0",
                "6.0",
                "5.0",
                "4.4",
                "",
            ],
            type=str,
            help="==> Mobile platform versions",
            default="14.5",
        )
        parser.add_argument(
            "--device_name",
            choices=Device.models,
            type=str,
            help="==> The device name models (check the platform version supported in --os_version)",
            default="local",
        )
        parser.add_argument(
            "--app_path",
            help="==> Relative or absolute path of an .APK or .IPA file (format is automatically recognized if --os arg is set)",
            default="",
        )
        parser.add_argument(
            "--orientation",
            choices=["Landscape", "Portrait"],
            help="==> Screen orientation for mobile executions (default = Portrait)",
            default="Portrait",
        )
        parser.add_argument(
            "--language",
            choices=Lang.language,
            help="==> Language to set for iOS (XCUITest driver only) and Android (default = )",
            default="en",
        )
        parser.add_argument(
            "--locale",
            choices=Lang.locale,
            help="==> Locale to set for iOS (XCUITest driver only) and Android. fr_CA format for iOS. CA format (country name abbreviation) for Android (default = )",
            default="",
        )
        parser.add_argument(
            "--tags",
            help="==> Feature(s) / Scenario(s) to be executed (separate tags by comma and without spaces)",
            default="",
        )
        parser.add_argument(
            "--exclude",
            choices=["wip", "skip", "bug", "slow", ""],
            help="==> Feature(s) / Scenario(s) to be ignored / skipped from execution using a single tag (recommended: wip)",
            default="",
        )
        args = parser.parse_args()
        return args

    @staticmethod
    def set_arguments(args):
        check_flags = (
            lambda arg_cmd, config_var: config_var
            if Conf.get_dev_mode().strip() == "true"
            else str(arg_cmd)
        )
        notify_running_mode = (
            Log.info(
                "<<<<< DEV MODE ENABLED: Using capabilities set from 'env_settings.properties' >>>>>\n"
            )
            if Conf.get_dev_mode().strip() == "true"
            else ""
        )
        flag_target = check_flags(args.target, Conf.get_debug_flag_target())
        flag_os = check_flags(args.os, Conf.get_debug_flag_os())
        flag_os_version = check_flags(args.os_version, Conf.get_debug_flag_os_version())
        flag_device_name = check_flags(args.device_name, Conf.get_debug_flag_device_name())
        flag_mode = check_flags(args.mode, Conf.get_debug_flag_mode())
        flag_orientation = check_flags(args.orientation, Conf.get_debug_flag_orientation())
        flag_language = check_flags(args.language, Conf.get_debug_flag_language())
        flag_locale = check_flags(args.locale, Conf.get_debug_flag_locale())
        flag_tags = check_flags(str(args.tags).rstrip(",").strip(), Conf.get_debug_behave_tags())
        flag_exclude = check_flags(
            str(args.exclude).rstrip(",").strip(), Conf.get_debug_behave_excluded_tags()
        )
        flag_environment = check_flags(args.environment, Conf.get_debug_flag_environment("staging"))

        Bctx.flag_mode.set(flag_mode)
        Bctx.flag_exclude.set(flag_exclude)
        Bctx.flag_os.set(flag_os)
        Bctx.flag_os_version.set(flag_os_version)
        Bctx.flag_device_name.set(flag_device_name)
        Bctx.flag_orientation.set(flag_orientation)
        Bctx.flag_language.set(flag_language)
        Bctx.flag_locale.set(flag_locale)
        Bctx.flag_tags.set(flag_tags)
        Bctx.flag_target.set(flag_target)
        Bctx.flag_environment.set(flag_environment)

        flag_mobile_app_path = (
            Conf.get_mobile_app_path()
            if str(args.target) != "remote_emulation"
            and (str(args.app_path) is None or str(args.app_path) == "")
            else str(args.app_path)
        )
        Bctx.flag_mobile_app_path.set(flag_mobile_app_path)

        Conf.show_logo()
        Log.info(
            f"Running with commands: \n\n \
                    EXECUTION TYPE: \n \
                    - Target = {Bctx.flag_target.get()} \n \
                    - Mode = {Bctx.flag_mode.get()} \n\n \
                    PLATFORM: \n \
                    - OS = {Bctx.flag_os.get()} \n \
                    - OS Version = {Bctx.flag_os_version.get()} \n \
                    - Device Name = {Bctx.flag_device_name.get()} \n \
                    APPLICATION: \n \
                    - Environment = {Bctx.flag_environment.get()} \n \
                    - Orientation (mobile) = {Bctx.flag_orientation.get()} \n \
                    - Language (device) = {Bctx.flag_language.get()} \n \
                    - Locale (device) = {Bctx.flag_locale.get()} \n \
                    - Mobile App Path (mobile: IPA / APK) = {Bctx.flag_mobile_app_path.get()} \n \
                    TESTS: \n \
                    - Behave Tag(s) = {Bctx.flag_tags.get()} \n \
                    - Behave Excluded Tags = {Bctx.flag_exclude.get()} \n"
        )

    @staticmethod
    def parse_behave_tags(tags_sequence=""):
        tags_sequence = Bctx.flag_tags.get()
        if tags_sequence is None or tags_sequence == "":
            return ""
        else:
            return "--tags=" + tags_sequence.replace(" ", "").replace("@", "").lower().strip() + " "
