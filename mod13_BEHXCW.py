import unittest
from datetime import datetime


def validate_symbol(symbol):
    if not isinstance(symbol, str):
        return False
    if not 1 <= len(symbol) <= 7:
        return False
    return symbol.isascii() and symbol.isalpha() and symbol.isupper()


def validate_chart_type(chart_type):
    if not isinstance(chart_type, str):
        return False
    return chart_type in ('1', '2')


def validate_time_series(time_series):
    if not isinstance(time_series, str):
        return False
    return time_series in ('1', '2', '3', '4')


def validate_date(date_text):
    if not isinstance(date_text, str):
        return False
    if len(date_text) != 10:
        return False
    try:
        datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        return False
    return True


class TestSymbol(unittest.TestCase):

    def test_valid_symbols(self):
        for symbol in ('A', 'GM', 'IBM', 'MSFT', 'GOOGL', 'ABCDEF', 'ABCDEFG'):
            self.assertTrue(validate_symbol(symbol), symbol)

    def test_lowercase_symbol(self):
        self.assertFalse(validate_symbol('ibm'))

    def test_mixed_case_symbol(self):
        self.assertFalse(validate_symbol('Msft'))

    def test_empty_symbol(self):
        self.assertFalse(validate_symbol(''))

    def test_symbol_too_long(self):
        self.assertFalse(validate_symbol('ABCDEFGH'))

    def test_symbol_with_numbers(self):
        self.assertFalse(validate_symbol('IBM1'))
        self.assertFalse(validate_symbol('123'))

    def test_symbol_with_special_characters(self):
        for symbol in ('BRK.B', 'BF-B', 'IB M', ' IBM', 'IBM ', 'IBM!', 'IBM\n'):
            self.assertFalse(validate_symbol(symbol), symbol)

    def test_symbol_not_a_string(self):
        for symbol in (None, 123, ['IBM'], True):
            self.assertFalse(validate_symbol(symbol), symbol)


class TestChartType(unittest.TestCase):

    def test_valid_chart_types(self):
        self.assertTrue(validate_chart_type('1'))
        self.assertTrue(validate_chart_type('2'))

    def test_chart_type_out_of_range(self):
        for chart_type in ('0', '3', '9', '-1'):
            self.assertFalse(validate_chart_type(chart_type), chart_type)

    def test_chart_type_more_than_one_character(self):
        for chart_type in ('11', '12', '01', '1.0', ' 1', '2 '):
            self.assertFalse(validate_chart_type(chart_type), chart_type)

    def test_chart_type_not_numeric(self):
        for chart_type in ('a', 'bar', 'line', '!', ''):
            self.assertFalse(validate_chart_type(chart_type), chart_type)

    def test_chart_type_not_a_string(self):
        for chart_type in (None, 1, 2, 1.0, True):
            self.assertFalse(validate_chart_type(chart_type), chart_type)


class TestTimeSeries(unittest.TestCase):

    def test_valid_time_series(self):
        for time_series in ('1', '2', '3', '4'):
            self.assertTrue(validate_time_series(time_series), time_series)

    def test_time_series_out_of_range(self):
        for time_series in ('0', '5', '9', '-1'):
            self.assertFalse(validate_time_series(time_series), time_series)

    def test_time_series_more_than_one_character(self):
        for time_series in ('10', '12', '04', '4.0', ' 3', '3 '):
            self.assertFalse(validate_time_series(time_series), time_series)

    def test_time_series_not_numeric(self):
        for time_series in ('a', 'daily', 'weekly', '!', ''):
            self.assertFalse(validate_time_series(time_series), time_series)

    def test_time_series_not_a_string(self):
        for time_series in (None, 1, 4, 2.0, True):
            self.assertFalse(validate_time_series(time_series), time_series)


class TestStartDate(unittest.TestCase):

    def test_valid_start_dates(self):
        for start_date in ('2023-03-01', '2000-01-01', '2024-02-29', '2025-12-31'):
            self.assertTrue(validate_date(start_date), start_date)

    def test_start_date_wrong_order(self):
        for start_date in ('03-01-2023', '01-03-2023', '2023-31-12'):
            self.assertFalse(validate_date(start_date), start_date)

    def test_start_date_wrong_separator(self):
        for start_date in ('2023/03/01', '2023.03.01', '20230301', '2023 03 01'):
            self.assertFalse(validate_date(start_date), start_date)

    def test_start_date_missing_leading_zeros(self):
        for start_date in ('2023-3-1', '2023-03-1', '2023-3-01', '23-03-01'):
            self.assertFalse(validate_date(start_date), start_date)

    def test_start_date_not_a_real_date(self):
        for start_date in ('2023-02-30', '2023-13-01', '2023-00-10', '2023-04-31', '2023-02-29'):
            self.assertFalse(validate_date(start_date), start_date)

    def test_start_date_not_a_date(self):
        for start_date in ('', 'today', 'March 1, 2023', '2023-03-01 10:00:00', ' 2023-03-01'):
            self.assertFalse(validate_date(start_date), start_date)

    def test_start_date_not_a_string(self):
        for start_date in (None, 20230301, ['2023-03-01']):
            self.assertFalse(validate_date(start_date), start_date)


class TestEndDate(unittest.TestCase):

    def test_valid_end_dates(self):
        for end_date in ('2023-03-30', '1999-12-31', '2020-02-29', '2026-01-01'):
            self.assertTrue(validate_date(end_date), end_date)

    def test_end_date_wrong_order(self):
        for end_date in ('03-30-2023', '30-03-2023', '2023-30-03'):
            self.assertFalse(validate_date(end_date), end_date)

    def test_end_date_wrong_separator(self):
        for end_date in ('2023/03/30', '2023.03.30', '20230330', '2023 03 30'):
            self.assertFalse(validate_date(end_date), end_date)

    def test_end_date_missing_leading_zeros(self):
        for end_date in ('2023-3-30', '2023-12-1', '2023-1-1', '23-03-30'):
            self.assertFalse(validate_date(end_date), end_date)

    def test_end_date_not_a_real_date(self):
        for end_date in ('2023-06-31', '2023-12-32', '2023-11-00', '2021-02-29', '0000-01-01'):
            self.assertFalse(validate_date(end_date), end_date)

    def test_end_date_not_a_date(self):
        for end_date in ('', 'tomorrow', 'March 30, 2023', '2023-03-30T00:00:00', '2023-03-30 '):
            self.assertFalse(validate_date(end_date), end_date)

    def test_end_date_not_a_string(self):
        for end_date in (None, 20230330, ['2023-03-30']):
            self.assertFalse(validate_date(end_date), end_date)


if __name__ == '__main__':
    unittest.main()
