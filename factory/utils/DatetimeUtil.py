import pytz
from datetime import datetime, timedelta
from dateutil.relativedelta import *


class DatetimeUtil:
    @staticmethod
    def get_current_date(string_format="%d/%m/%Y"):
        """Get current date / time formatted
        %a: Returns the first three characters of the weekday, e.g. Wed.
        %b: Returns the first three characters of the month, e.g. Mar.
        %A: Returns the full name of the weekday, e.g. Wednesday.
        %B: Returns the full name of the month, e.g. September.
        %w: Returns the weekday as a number, from 0 to 6, with Sunday being 0.
        %m: Returns the month as a number, from 01 to 12.
        %p: Returns AM/PM for time.
        %y: Returns the year in two-digit format, that is, without the century. For example, "18" instead of "2018".
        %f: Returns microsecond from 000000 to 999999.
        %Z: Returns the timezone.
        %z: Returns UTC offset.
        %j: Returns the number of the day in the year, from 001 to 366.
        %W: Returns the week number of the year, from 00 to 53, with Monday being counted as the first day of the week.
        %U: Returns the week number of the year, from 00 to 53, with Sunday counted as the first day of each week.
        %c: Returns the local date and time version.
        %x: Returns the local version of date.
        %X: Returns the local version of time.

        Args:
            string_format (str): Format of date passed.

        Returns:
            str: String of current date according the format you provided
        """
        return datetime.now().strftime(string_format)

    @staticmethod
    def get_current_time():
        return datetime.now().strftime("%H:%M:%S")

    @staticmethod
    def format_datetime_to(date_string, old_format="%d/%m/%Y", new_format=""):
        old_datetime = datetime.strptime(date_string, old_format)
        new_datetime = datetime.strftime(old_datetime, new_format)
        return new_datetime

    @staticmethod
    def to_timestamp_format(timestamp=True, timezone=True):
        datetime_micsecs = "%Y-%m-%dT%H:%M:%S.%f"
        add_tz = "%z" if timezone else ""
        return f"{datetime_micsecs}{add_tz}"

    @staticmethod
    def get_period_of_day(timezone_region):
        now = datetime.now().replace(microsecond=0)
        timezone_region = timezone_region if timezone_region is not None else "Europe/London"
        converted_tz = now.astimezone(pytz.timezone(timezone_region))
        morning_t = converted_tz.replace(hour=5, minute=0, second=0, microsecond=0)
        morning_t1 = converted_tz.replace(hour=11, minute=59, second=59, microsecond=0)
        afternoon_t = converted_tz.replace(hour=12, minute=0, second=0, microsecond=0)
        afternoon_t1 = converted_tz.replace(hour=16, minute=59, second=59, microsecond=0)
        print(f"-> Machine time: {converted_tz}")
        if morning_t <= converted_tz <= morning_t1:
            return "morning"
        elif afternoon_t <= converted_tz <= afternoon_t1:
            return "afternoon"
        else:
            return "evening"

    @staticmethod
    def plus_date(
        date_string_d_m_y, plus_days=0, plus_months=0, plus_years=0, new_format="%d/%m/%Y"
    ):
        date_split = str(date_string_d_m_y).split("/")
        day_ = int(date_split[0])
        month_ = int(date_split[1])
        year_ = int(date_split[2]) + int(plus_years)
        datetime(year_, month_, day_)
        date_calculated = (
            datetime(year_, month_, day_)
            + timedelta(days=int(plus_days))
            + relativedelta(months=int(plus_months))
        )
        return date_calculated.strftime(new_format)

    @staticmethod
    def reduce_date(
        date_string_d_m_y, minus_days=0, minus_months=0, minus_years=0, new_format="%d/%m/%Y"
    ):
        date_split = str(date_string_d_m_y).split("/")
        day_ = int(date_split[0])
        month_ = int(date_split[1])
        year_ = int(date_split[2]) - int(minus_years)
        datetime(year_, month_, day_)
        date_calculated = (
            datetime(year_, month_, day_)
            - timedelta(days=int(minus_days))
            - relativedelta(months=int(minus_months))
        )
        return date_calculated.strftime(new_format)

    @staticmethod
    def calculate_difference_between_dates(early_date, later_date="", is_later_date_today=False):
        format_dates = "%d/%m/%Y"
        old = datetime.strptime(early_date, format_dates)
        current_date = DatetimeUtil.get_current_date("%d/%m/%Y")
        recent = (
            datetime.strptime(current_date, format_dates)
            if is_later_date_today
            else datetime.strptime(later_date, format_dates)
        )
        difference = relativedelta(old, recent)
        diff_dates = {
            "years": abs(difference.years),
            "months": abs(difference.months),
            "days": abs(difference.days),
            "minutes": abs(difference.minutes),
            "seconds": abs(difference.seconds),
            "microsecs": abs(difference.microseconds),
        }
        return diff_dates
