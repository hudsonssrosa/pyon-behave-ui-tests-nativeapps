import os
from factory.base_context import BaseContext as Bctx
from factory.handling.base_logging import BaseLogging as Log
from factory.utils.OsUtil import OsUtil
from factory.utils.FileUtil import FileUtil

"""    ATTENTION: Insert additional command parameters in 'behave.ini'  file
       Allure Source 2.13.2: "https://github.com/allure-framework/allure2/releases/tag/2.13.2"
"""
allure_report_dir = "allure-report"
allure_results_dir = "allure-results"
dot_allure_results_dir = f".{os.sep}{allure_results_dir}"


class AllureReport:
    @staticmethod
    def set_screenshot_path(path=""):
        Bctx.screenshot_path.set(path)
        return Bctx.screenshot_path.get()

    @staticmethod
    def get_environment():
        return f"-{Bctx.flag_environment.get()}"

    @staticmethod
    def cleanup_reports(generate_report=True):
        if generate_report:
            deletion_message = " directory deleted successfully!"
            FileUtil.remove_files(deletion_message, allure_report_dir)
            FileUtil.remove_files(
                deletion_message, dot_allure_results_dir + AllureReport.get_environment()
            )

    @staticmethod
    def generate_report_command(generate_report=True, allure_lib_path=""):
        if generate_report:
            Log.info("Generating Allure Report...")
            if OsUtil.has_os_platform_name("linux") or OsUtil.has_os_platform_name("darwin"):
                os.system(f"chmod 777 {allure_lib_path}")
            """ Full Command: $ python ./.resources/allure-2.13.2/bin/allure generate -o allure-report ./allure-results """
            os.system(
                f"{allure_lib_path} generate -o {allure_report_dir} {dot_allure_results_dir}{AllureReport.get_environment()}"
            )

    @staticmethod
    def open_report_command_locally(generate_report=True, allure_lib_path=""):
        if generate_report:
            """ Full Command: $ python ./.resources/allure-2.13.2/bin/allure open allure-report """
            os.system(f"{allure_lib_path} open {allure_report_dir}")
            Log.info(
                f"See the reports results in: "
                + OsUtil.search_file_in_root_dir(os.sep + allure_report_dir, "index.html")
            )
