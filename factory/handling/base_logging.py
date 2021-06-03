import json
import logging
from factory.utils.StringsUtil import StringUtil
from factory.utils.TextColorUtil import TextColor as Color

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)


class BaseLogging:
    @staticmethod
    def display_debug_error(message):
        logging.basicConfig(
            level=logging.ERROR, format="[%(levelname)-2s %(asctime)s]: %(message)s"
        )
        logging.error(Color.red("   ERROR: {}".format(message)), exc_info=True)

    @staticmethod
    def display_debug_log():
        logging.basicConfig(
            level=logging.DEBUG, format="[%(levelname)-2s %(asctime)s]: %(message)s"
        )

    @staticmethod
    def show_response(response, show_header=False):
        try:
            if show_header:
                BaseLogging.info("-- HEADER --")
                print(Color.blue(response.headers) + "\n")
            parsed_body = json.loads(str(response.text))
            BaseLogging.info("-- RESPONSE BODY --")
            print(Color.blue(StringUtil.indent_dict_body(parsed_body)))
        except Exception as ex:
            message = BaseLogging.show_exception(
                "EXCEPTION: ", "It does not possible to get the response body! ", ex
            )
            BaseLogging.error(message)
            raise Exception(message)

    @staticmethod
    def status_passed():
        print(Color.green("   >>>>>>> STEP PASSED! ᕦ︵( ^ ͜ʖ^ )︵ᕤ <<<<<<<\n"))

    @staticmethod
    def status_failed(stacktrace=""):
        print(Color.red(f"   ERROR IN: {stacktrace}"))
        print(Color.red("\n   >>>>>>> STEP FAILED! 乁_(´ʘ ʖ̯ʘ`)_ㄏ <<<<<<<\n"))

    @staticmethod
    def error(message="", display_msg_config=False):
        print(Color.red(f"   ERROR :: {message}"))
        if display_msg_config:
            BaseLogging.display_debug_error(message)

    @staticmethod
    def warning(message=""):
        print(Color.yellow(f"   WARN :: {message}"))

    @staticmethod
    def info(message=""):
        print(Color.blue(f"\n   :: {message}"))

    @staticmethod
    def success(message=""):
        print(Color.green(f"   :: (\u2713) {message}"))

    @staticmethod
    def show_exception(title, custom_message, exception):
        message = f"\n{BaseLogging.create_header_with_top_marker(title, custom_message, '', '-')}\n\n(+)Causes:\n{exception}"
        return message

    @staticmethod
    def gherkin_feature_info(feature_data):
        print(
            "\n"
            + Color.magenta(
                BaseLogging.create_header_with_top_marker(
                    title="", text=feature_data, ends_with="", marker="^"
                )
            )
        )

    @staticmethod
    def gherkin_scenario_info(scenario_data):
        print(
            "\n"
            + Color.magenta(
                BaseLogging.create_header_with_top_marker(
                    title="", text=scenario_data, ends_with=" :", marker="-"
                )
            )
        )

    @staticmethod
    def gherkin_step_info(step_data):
        print(
            Color.cyan(
                BaseLogging.create_header_statement(
                    title="   └--- STEP ", text=step_data, ends_with=" :"
                )
            )
        )

    @staticmethod
    def get_marker_from_a_text_length(text, marker):
        string_length = str(text).__len__()
        count_str = 0
        new_string = "└"
        for i in range(0, string_length):
            count_str = count_str + i
            new_string = new_string + str(marker)
        return new_string

    @staticmethod
    def create_header_statement(title, text, ends_with):
        return f"{str(title).upper()}{text}{ends_with}"

    @staticmethod
    def create_header_with_top_marker(title, text, ends_with, marker):
        return (
            BaseLogging.get_marker_from_a_text_length(str(title) + str(text), marker)
            + "\n"
            + BaseLogging.create_header_statement(title, text, ends_with)
        )
