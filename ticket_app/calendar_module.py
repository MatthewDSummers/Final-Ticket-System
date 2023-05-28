
from datetime import datetime, date, timedelta
import pytz
# from datetime import date, datetime, timedelta

MONTHS = {
    "01":"January", "02":"February", "03":"March", "04":"April", 
    "05":"May", "06":"June", "07":"July", "08":"August", "09":"September",
    "10":"October", "11":"November", "12":"December"
}
def get_formatted_dates(date_list):
    if not isinstance(date_list, list):
        date_list = [date_list]

    formatted_dates = []

    for date_str in date_list:
        date = date_str.strip()
        try:
            date_obj = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Date string not in correct format (YYYY-MM-DD)")

    # get just the DAY portion, remove any leading 0's and replace
        formatted_day = date_obj.strftime("%d").lstrip("0")
    # do the same for the month and retrieve it from the MONTHS dictionary
        formatted_month = MONTHS[date_obj.strftime("%m")]
    # get just the YEAR portion
        formatted_year = date_obj.strftime("%Y")

    # Suffix is "th" if the DAY portion is 11 to 13, otherwise the modulus 10 will get just the number (in case of single digits) or the 2nd digit of the number (in case of double digit days),
    # then use it as the key to retrieve the desired suffix value from the created dictionary.
    # If the digit (key) is not present in the dict, it will use the default suffix "th".
        suffix = "th" if int(formatted_day) >= 11 and int(formatted_day) <= 13 else {1: "st", 2: "nd", 3: "rd"}.get((int(formatted_day) % 10), "th")

    # add the suffix to the day
        formatted_day += suffix
        formatted_dates.append((f"{formatted_month} {formatted_day}, {formatted_year}"))
    return formatted_dates

def get_aware_date(start_date, end_date=None):
    # timezone = pytz.timezone('Europe/London')
    timezone = pytz.timezone('US/Eastern')

    start_date = start_date.strip()
    start_date = timezone.localize(datetime.strptime(start_date, "%Y-%m-%d"))

    if end_date:
        end_date = end_date.strip()
        end_date = timezone.localize(datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1))
        return [start_date, end_date]
    else:
        return start_date