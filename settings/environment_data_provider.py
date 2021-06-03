import os
from factory.base_context import BaseContext as Bctx
from sys import platform as _platform
from factory.utils.OsUtil import OsUtil
from factory.utils.FileUtil import FileUtil
from factory.utils.TextColorUtil import TextColor as Color


ENV_SETTINGS = "env_settings"
LINUX_OR_IOS = _platform == "linux" or _platform == "linux2" or _platform == "darwin"
WINDOWS = _platform == "win32" or "win64"
UTF8_UPPER = "UTF-8"
UTF8 = "utf-8"
SEP = os.sep


def read_env_conf_properties_to_os_platform(file_name):
    if LINUX_OR_IOS:
        return FileUtil.read_properties(
            [OsUtil.search_file_in_root_dir(OsUtil.get_current_dir_name(), file_name)]
        )
    elif WINDOWS:
        return FileUtil.read_properties(
            [OsUtil.search_file_in_root_dir(OsUtil.get_current_dir(), file_name)]
        )


CONFIG = read_env_conf_properties_to_os_platform(ENV_SETTINGS + ".properties")


class EnvSettings:
    @staticmethod
    def get_screenshot_path():
        from factory.handling.allure_report_impl import allure_report_dir

        return str(f"{allure_report_dir}{SEP}screenshots")

    @staticmethod
    def __check_mobile_app_format(platform, path):
        if platform == "Android":
            return ".apk"
        else:
            return ".ipa" if ".app" not in path else ""

    # ---- REPORT PARAMETERS ----
    @staticmethod
    def get_report_library_path():
        report_lib_path = os.path.abspath(CONFIG.get("report", "report_library_path"))
        return report_lib_path.replace("\\", SEP).strip()

    @staticmethod
    def get_generate_report():
        report_enabled = CONFIG.get("report", "generate_report", fallback=None)
        return str(report_enabled).strip() == "true"

    # ---- DEFAULT PARAMETERS ----
    @staticmethod
    def get_url_app_dev():
        return CONFIG.get("default", "app_url_dev").strip()

    @staticmethod
    def get_admin_url_dev():
        return CONFIG.get("default", "admin_app_url_dev").strip()

    @staticmethod
    def get_url_app_staging():
        return CONFIG.get("default", "app_url_staging").strip()

    @staticmethod
    def get_admin_url_staging():
        return CONFIG.get("default", "admin_app_url_staging").strip()

    @staticmethod
    def get_url_app_prod():
        return CONFIG.get("default", "app_url_prod").strip()

    @staticmethod
    def get_admin_url_prod():
        return CONFIG.get("default", "admin_app_url_prod").strip()

    @staticmethod
    def get_email_url():
        return CONFIG.get("default", "email_validation_url").strip()

    @staticmethod
    def get_internal_resources_webdriver_dir():
        return str(f".resources{SEP}webdrivers_for_automation")

    # ---- DEBUG PARAMETERS ----
    @staticmethod
    def get_dev_mode():
        return CONFIG.get("cli-args-debug", "development_mode", fallback=None)

    @staticmethod
    def get_debug_flag_environment(default_env):
        env_config = CONFIG.get("cli-args-debug", "debug_flag_environment", fallback=None)
        environment_set = default_env if env_config is None else env_config
        return environment_set

    @staticmethod
    def get_debug_flag_target():
        return str(CONFIG.get("cli-args-debug", "debug_flag_target", fallback=None).strip())

    @staticmethod
    def get_debug_flag_mode():
        return str(CONFIG.get("cli-args-debug", "debug_flag_mode", fallback=None).strip())

    @staticmethod
    def get_debug_behave_tags():
        return CONFIG.get("cli-args-debug", "debug_behave_tags", fallback=None)

    @staticmethod
    def get_debug_behave_excluded_tags():
        return CONFIG.get("cli-args-debug", "debug_behave_excluded_tags", fallback=None)

    @staticmethod
    def get_debug_flag_os():
        return str(CONFIG.get("cli-args-debug", "debug_flag_os", fallback=None).strip())

    @staticmethod
    def get_debug_flag_os_version():
        return str(CONFIG.get("cli-args-debug", "debug_flag_os_version", fallback=None).strip())

    @staticmethod
    def get_debug_flag_device_name():
        return str(CONFIG.get("cli-args-debug", "debug_flag_device_name", fallback=None).strip())

    @staticmethod
    def get_debug_flag_orientation():
        return str(CONFIG.get("cli-args-debug", "debug_flag_orientation", fallback=None).strip())

    @staticmethod
    def get_debug_flag_language():
        return CONFIG.get("cli-args-debug", "debug_flag_language", fallback=None)

    @staticmethod
    def get_debug_flag_locale():
        return CONFIG.get("cli-args-debug", "debug_flag_locale", fallback=None)

    # ---- BROWSERSTACK PARAMETERS ----
    @staticmethod
    def get_bs_user_key():
        return CONFIG.get("browserstack", "bs_user_key")

    @staticmethod
    def get_bs_access_key():
        return CONFIG.get("browserstack", "bs_access_key", fallback=None)

    @staticmethod
    def get_bs_record_video():
        return CONFIG.get("browserstack", "bs_record_video").strip()

    # ---- REAL DEVICE PARAMETERS ----
    @staticmethod
    def get_appium_host_ip():
        return CONFIG.get("default-device", "appium_host_ip", fallback=None)

    @staticmethod
    def get_appium_host_port():
        return CONFIG.get("default-device", "appium_host_port", fallback=None)

    @staticmethod
    def get_mobile_automation_name():
        return CONFIG.get("default-device", "mobile_automation_name", fallback=None)

    @staticmethod
    def get_mobile_app_path():
        path = (
            os.path.abspath(CONFIG.get("default-device", "mobile_app_path"))
            .replace("\\", SEP)
            .replace("/", SEP)
            .replace(".ipa", "")
            .replace(".apk", "")
            .strip()
        )
        platform = Bctx.flag_os.get()
        app_format_on_platform = EnvSettings.__check_mobile_app_format(platform, path)
        return path + app_format_on_platform

    @staticmethod
    def get_xcode_webdriveragent_path():
        return CONFIG.get("local-device", "xcode_local_webdriveragent").replace("\\", SEP).strip()

    @staticmethod
    def get_xcode_webdriveragent_bootstrap_path():
        full_path = CONFIG.get("local-device", "xcode_local_webdriveragent").strip()
        return FileUtil.remove_last_element_from_path(full_path)

    @staticmethod
    def show_logo():
        logo = Color.green(
            """
                                                  █                                                             
                                █████████.     :██                                                             
                             █████      ███    ███                                                              
                           ███           ██   ██                 .█.                                            
                         ███             ██  ██               █████████                ,█:                      
                       ███              :█: ██               ██       :██           :███████                    
                      ██               ███  ██        ████  ██     ███  ███       ███,    ,█:   ,████:          
                    :██              ███:   ██      ███ ,█  ██       ██   ██    ███        ██ ████::█████:      
                   ███         :██████      ███ :████   ██   ██     :█:    ██:███          ,███          ███:   
                  ███                        :████     ██     ████████      ███                            :██: 
                 ██:                                  ██        `█´                                          : 
                ██:                                  ██                                                         
               :██                                  ██       ,████    █████   █      █  ,███  █        █ █████  
               ██                                 ,██       █     █  █     █ █      █  █   `█ █      █  █     █ 
              ██                                 ███        █    █  █     █  █      █     .██  █    █  █     █  
             ██                                 ███         █████   █:.███  :███████   ███´¨█   █  █   █.:███   
             ██                                ██          █     █  ██:     █      █  █     █    ██    ██´      
            ██                               :██           █    ,█  █   ,█  █      █ █,    █     █     █   ,█   
            █                                +█           .█████´   `███´  █      █   `███´      |     `███´   
                
                   PYON BEHAVE - UI Test Automation for Native Apps | Created by: Hudson S. S. Rosa 
            """
        )
        """ Generated with http://manytools.org/hacker-tools/convert-images-to-ascii-art/go/ """
        return print(logo)
