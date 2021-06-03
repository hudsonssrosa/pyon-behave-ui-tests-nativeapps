import io
import requests
from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from factory.handling.base_logging import BaseLogging as Log
from factory.handling.running_exception import RunningException as Rexc
from factory.utils.StringsUtil import StringUtil as String
from factory.base_context import BaseContext as Bctx


spc = " " * 10


class Assertion(str):
    def __init__(self, comparative_value):
        super().__init__()
        self.comparative_value = comparative_value

    def is_equals_to(
        self,
        value_expected,
        optional_description="",
    ):
        expected = (
            str(value_expected).replace("_RANDOM_DATA_", Bctx.random_data.get()).strip()
            if str(value_expected).__contains__("_RANDOM_DATA_")
            else str(value_expected).strip()
        )
        label = str(self.comparative_value).strip()
        try:
            assert expected == label
            if label == expected:
                Log.success(
                    f"{optional_description}\n{spc}--> EXPECTED: [{expected}]\n{spc}└-> FOUND: [{label}]"
                )
        except AssertionError as ae:
            Rexc.raise_assertion_error(
                f"(X) {optional_description}\n{spc}--> EXPECTED: [{expected}],\n{spc}└-> BUT FOUND: [{label}]",
                ae,
            )

    def is_greater_than(self, b_value, optional_description=""):
        a_value = String.convert_currency_to_number(float(self.comparative_value))
        b_value = String.convert_currency_to_number(float(b_value))
        try:
            assert a_value > b_value
            if a_value > b_value:
                Log.success(
                    f"{optional_description}{spc}--> [{a_value}]  IS GREATER THAN  [{b_value}]"
                )
        except AssertionError as ae:
            Rexc.raise_assertion_error(
                f"(X) {optional_description}{spc}--> [{a_value}],  BUT IS NOT GREATER THAN  [{b_value}]",
                ae,
            )

    def is_less_than(self, b_value, optional_description=""):
        a_value = String.convert_currency_to_number(float(self.comparative_value))
        b_value = String.convert_currency_to_number(float(b_value))
        try:
            assert a_value < b_value
            if a_value < b_value:
                Log.success(
                    f"{optional_description}{spc}--> [{a_value}]  IS LESS THAN  [{b_value}]"
                )
        except AssertionError as ae:
            Rexc.raise_assertion_error(
                f"(X) {optional_description}{spc}--> [{a_value}],  BUT IS NOT LESS THAN  [{b_value}]",
                ae,
            )

    def is_different_from(self, b_value, optional_description=""):
        a_value = String.convert_currency_to_number(float(self.comparative_value))
        b_value = String.convert_currency_to_number(float(b_value))
        try:
            assert a_value != b_value
            if a_value != b_value:
                Log.success(
                    f"{optional_description}{spc}--> [{a_value}]  IS DIFFERENT FROM  [{b_value}]"
                )
        except AssertionError as ae:
            Rexc.raise_assertion_error(
                f"(X) {optional_description}{spc}--> [{a_value}],  BUT IS NOT DIFFERENT FROM  [{b_value}]",
                ae,
            )

    def contains_the(
        self,
        value_expected,
        optional_description="",
    ):
        expected = (
            str(value_expected).replace("_RANDOM_DATA_", Bctx.random_data.get()).lower().strip()
            if str(value_expected).__contains__("_RANDOM_DATA_")
            else str(value_expected).lower().strip()
        )
        found = str(self.comparative_value).lower().strip()
        found_display_1000_chars = (
            str(self.comparative_value[:1000]).lower().strip()
            if len(self.comparative_value) > 1000
            else found
        )
        try:
            if found == "" or expected == "":
                return
            else:
                assert expected in found or found in expected
                if expected in found or found in expected:
                    Log.success(
                        f"{optional_description}\n{spc}--> [{expected}]\n{spc}└-> MATCHES WITH [{found_display_1000_chars}]"
                    )
        except AssertionError as ae:
            Rexc.raise_assertion_error(
                f"(X) {optional_description}\n{spc}--> [{expected}],\n{spc}└-> BUT DOES NOT MATCH WITH: [{found_display_1000_chars}]",
                ae,
            )

    def is_between_the(self, expected_min, expected_max, optional_description=""):
        item = int(self.comparative_value)
        max_no = int(expected_max)
        min_no = int(expected_min)
        try:
            assert min_no <= item <= max_no
            if min_no <= item <= max_no:
                Log.success(
                    f"{optional_description}{spc}--> [{item}]  IS BETWEEN  [{min_no}] AND [{max_no}]"
                )
        except AssertionError as ae:
            Rexc.raise_assertion_error(
                f"(X) {optional_description}{spc}--> [{item}]  IS NOT BETWEEN  [{min_no}] AND [{max_no}]",
                ae,
            )

    def is_present(self, optional_description=""):
        element = int(self.comparative_value)
        is_element_present = element is True or element == True
        try:
            assert is_element_present
            if is_element_present:
                Log.success(f"{optional_description}{spc}--> [{element}]  IS PRESENT]")
        except AssertionError as ae:
            Rexc.raise_assertion_error(
                f"(X) {optional_description}{spc}--> [{element}]  IS NOT PRESENT]",
                ae,
            )

    def is_not_present(self, optional_description=""):
        element = int(self.comparative_value)
        is_element_not_present = element is False or element == False
        try:
            assert is_element_not_present
            if is_element_not_present:
                Log.success(f"{optional_description}{spc}--> [{element}]  IS NOT PRESENT]")
        except AssertionError as ae:
            Rexc.raise_assertion_error(
                f"(X) {optional_description}{spc}--> [{element}]  IS PRESENT]",
                ae,
            )

    def is_in_strings_list(self, list_of_strings_expected, optional_description=""):
        expected_items_list = [str(y).lower() for y in list_of_strings_expected]
        for item in self.comparative_value:
            if str(item).lower() in expected_items_list:
                self.contains_the(str(item).lower(), optional_description)

    def is_in_pdf(self, pdf_file_path, fragment_content, optional_description=""):
        file = io.BytesIO(requests.get(pdf_file_path).content)
        output_string = StringIO()
        parser = PDFParser(file)
        doc = PDFDocument(parser)
        resource_manager = PDFResourceManager()
        device = TextConverter(resource_manager, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(resource_manager, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
        self.comparative_value = "".join(
            [str(elem).strip(" ") for elem in output_string.getvalue().split("\n")]
        ).replace("\t", " ")
        self.contains_the(fragment_content, optional_description)