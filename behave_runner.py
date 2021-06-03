import sys, os
from behave.__main__ import main as behave_main
from factory.base_context import BaseContext as Bctx
from factory.handling.base_logging import BaseLogging as Log

from settings.cli_impl import Cli
from settings.environment_data_provider import EnvSettings as Conf
from factory.handling.allure_report_impl import AllureReport


allure_results_dir = "./allure-results"


def main():
    args = Cli.parse_external_args()
    Cli.set_arguments(args)
    try:
        execute_commands()
    except:
        return 1


def execute_commands():
    try:
        AllureReport.set_screenshot_path(Conf.get_screenshot_path())
        AllureReport.cleanup_reports(Conf.get_generate_report())
        run_behave_allure_command()
    finally:
        if Bctx.flag_target.get() != "remote_emulation":
            AllureReport.generate_report_command(
                Conf.get_generate_report(), Conf.get_report_library_path()
            )
            AllureReport.open_report_command_locally(
                Conf.get_generate_report(), Conf.get_report_library_path()
            )


def run_behave_allure_command():
    env_selected = Bctx.flag_environment.get()
    environment_features = os.path.abspath(f"features{os.sep}feature_domains{os.sep}{env_selected}")
    environment_features_result = str(environment_features).replace(f"{os.sep}fastlane", "")
    Log.info(f"Running Behave tests in {env_selected}...")
    tags = Cli.parse_behave_tags()
    allure_results_env = f"{allure_results_dir}-{env_selected}"
    result = behave_main(
        f"{tags}-f allure_behave.formatter:AllureFormatter -o {allure_results_env} -k {environment_features_result}"
    )
    if result == 1:
        raise BaseException


class BehaveRunner:
    if __name__ == "__main__":
        sys.exit(main())
