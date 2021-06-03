import locale
import json
import re


class StringUtil:
    @staticmethod
    def retrieve_data_context(existing_context, fallback=""):
        try:
            return (
                fallback
                if existing_context is None or existing_context == "None"
                else existing_context
            )
        except:
            return fallback

    @staticmethod
    def is_not_blank_or_null(value):
        if value is not None or value != "":
            return value

    @staticmethod
    def join_long_wrapped_text(raw_text):
        return "".join([str(elem).strip(" ") for elem in raw_text.split("\n")])

    @staticmethod
    def indent_dict_body(dictionary):
        return json.dumps(dictionary, sort_keys=True, indent=4)

    @staticmethod
    def format_decimal_places(decimal_number, no_of_places=2):
        switcher = {
            0: "{:.0f}".format(decimal_number),
            1: "{:.1f}".format(decimal_number),
            2: "{:.2f}".format(decimal_number),
            3: "{:.3f}".format(decimal_number),
        }
        return switcher.get(int(no_of_places))

    @staticmethod
    def format_month_number_to_name(number_of_month):
        months = [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ]
        return months[int(number_of_month) - 1]

    @staticmethod
    def format_ordinal_number(number):
        switcher = {0: "th", 1: "st", 2: "nd", 3: "rd"}
        return str(number) + switcher.get(int(number), "th")

    @staticmethod
    def extract_number(value):
        return "".join(filter(lambda i: i.isdigit(), str(value)))

    @staticmethod
    def extract_decimal(value):
        return re.findall("\d*\.?\d+", str(value))

    @staticmethod
    def format_number_separators(value_to_format):
        return "{:,.2f}".format(float(value_to_format))

    @staticmethod
    def set_currency_locale(default_locale="en_GB.UTF-8"):
        locale.setlocale(locale.LC_ALL, default_locale)

    @staticmethod
    def parse_number_to_currency(value_to_format, cur_symbol=True):
        StringUtil.set_currency_locale()
        return locale.currency(
            float(value_to_format), symbol=cur_symbol, grouping=True, international=False
        )

    @staticmethod
    def parse_currency_to_number(value_to_format, cur_symbol=""):
        return locale.atof(str(value_to_format).strip(cur_symbol))

    @staticmethod
    def convert_number_to_currency(
        value_to_format, thousands_separator=",", fractional_separator=".", currency="£"
    ):
        amount = float(value_to_format)
        currency_value = currency + "{:,.2f}".format(amount)
        if thousands_separator == ".":
            main_currency, fractional_currency = (
                currency_value.split(".")[0],
                currency_value.split(".")[1],
            )
            new_main_currency = main_currency.replace(",", ".")
            currency_value = new_main_currency + fractional_separator + fractional_currency
        return currency_value

    @staticmethod
    def convert_currency_to_number(value_to_format):
        number = re.sub("[^0-9|.]", "", str(value_to_format))
        return float(number)

    @staticmethod
    def remove_multispaces(value_to_format):
        return " ".join(str(value_to_format).split())

    @staticmethod
    def correct_link_bar(link):
        """Normalise URL slashes

        Args:
            link (str): Inform the URL or path to normalise any duplicated slashes

        Returns:
            str: Normalised path / URL
        """
        url_or_path = f"{link}".split("://")
        result = f'{url_or_path[0]}://{url_or_path[1].replace("//", "/")}'
        return result
