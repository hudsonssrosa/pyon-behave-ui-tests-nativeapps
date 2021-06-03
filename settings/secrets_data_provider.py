import os
from sys import platform as _platform
from factory.utils.OsUtil import OsUtil
from factory.utils.FileUtil import FileUtil


LINUX_OR_IOS = _platform == "linux" or _platform == "linux2" or _platform == "darwin"
WINDOWS = _platform == "win32" or "win64"
UTF8_UPPER = "UTF-8"
UTF8 = "utf-8"
SEP = os.sep


class SecretsSettings:
    @staticmethod
    def __read_env_conf_properties_to_os_platform(file_name):
        try:
            if LINUX_OR_IOS:
                return FileUtil.read_properties(
                    [OsUtil.search_file_in_root_dir(OsUtil.get_current_dir_name(), file_name)]
                )
            elif WINDOWS:
                return FileUtil.read_properties(
                    [OsUtil.search_file_in_root_dir(OsUtil.get_current_dir(), file_name)]
                )
        except:
            return "File not found"

    @staticmethod
    def _fetch_config(section, property_key):
        try:
            config = SecretsSettings.__read_env_conf_properties_to_os_platform(
                "pyon_secret_data.properties"
            )
            return config.get(section, property_key)
        except Exception as ex:
            return "Property not found."

    @staticmethod
    def get_secret_app_user():
        return SecretsSettings._fetch_config("app-auth", "PYON_SECRET_APP_USER_NAME").strip()

    @staticmethod
    def get_secret_app_pass():
        return SecretsSettings._fetch_config("app-auth", "PYON_SECRET_APP_PASS").strip()

    @staticmethod
    def get_secret_configcat_sdk_key_ff_dev():
        return SecretsSettings._fetch_config(
            "app-configcat", "PYON_SECRET_CONFIGCAT_SDK_KEY_FF_DEV"
        ).strip()

    @staticmethod
    def get_secret_configcat_sdk_key_ff_staging():
        return SecretsSettings._fetch_config(
            "app-configcat", "PYON_SECRET_CONFIGCAT_SDK_KEY_FF_STAGING"
        ).strip()

    @staticmethod
    def get_secret_configcat_sdk_key_ff_production():
        return SecretsSettings._fetch_config(
            "app-configcat", "PYON_SECRET_CONFIGCAT_SDK_KEY_FF_PRODUCTION"
        ).strip()
