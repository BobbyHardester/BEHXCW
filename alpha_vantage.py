import os
from datetime import datetime

import requests

API_URL = os.environ.get('ALPHA_VANTAGE_URL', 'https://www.alphavantage.co/query')

TIME_SERIES = {
    '1': {'label': 'Intraday', 'function': 'TIME_SERIES_INTRADAY', 'key': 'Time Series (60min)'},
    '2': {'label': 'Daily', 'function': 'TIME_SERIES_DAILY', 'key': 'Time Series (Daily)'},
    '3': {'label': 'Weekly', 'function': 'TIME_SERIES_WEEKLY', 'key': 'Weekly Time Series'},
    '4': {'label': 'Monthly', 'function': 'TIME_SERIES_MONTHLY', 'key': 'Monthly Time Series'},
}


class ApiError(Exception):
    pass


def build_params(symbol, choice, api_key, full):
    series = TIME_SERIES[choice]
    params = {'function': series['function'], 'symbol': symbol, 'apikey': api_key}
    if choice == '1':
        params['interval'] = '60min'
    if choice in ('1', '2') and full:
        params['outputsize'] = 'full'
    return params


def request_json(params):
    try:
        response = requests.get(API_URL, params=params, timeout=30)
    except requests.RequestException:
        raise ApiError('Could not reach the Alpha Vantage API. Check the internet connection and try again.')
    if response.status_code != 200:
        raise ApiError('The Alpha Vantage API returned status {}.'.format(response.status_code))
    try:
        payload = response.json()
    except ValueError:
        raise ApiError('The Alpha Vantage API returned a response that could not be read.')
    if not isinstance(payload, dict):
        raise ApiError('The Alpha Vantage API returned a response that could not be read.')
    return payload


def fetch_time_series(symbol, choice, api_key):
    series = TIME_SERIES[choice]
    payload = request_json(build_params(symbol, choice, api_key, True))
    if series['key'] not in payload and 'Information' in payload and choice in ('1', '2'):
        payload = request_json(build_params(symbol, choice, api_key, False))

    if 'Error Message' in payload:
        raise ApiError('Alpha Vantage does not have data for the symbol {}.'.format(symbol))
    if 'Note' in payload:
        raise ApiError(payload['Note'])
    if series['key'] not in payload:
        if 'Information' in payload:
            raise ApiError(payload['Information'])
        raise ApiError('The Alpha Vantage API did not return any {} data.'.format(series['label'].lower()))

    return payload[series['key']]


def parse_stamp(stamp):
    for pattern in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d'):
        try:
            return datetime.strptime(stamp, pattern)
        except ValueError:
            continue
    return None


def filter_by_date(data, start_date, end_date):
    rows = []
    for stamp, values in data.items():
        moment = parse_stamp(stamp)
        if moment is None or not start_date <= moment.date() <= end_date:
            continue
        try:
            rows.append({
                'label': stamp,
                'moment': moment,
                'open': float(values['1. open']),
                'high': float(values['2. high']),
                'low': float(values['3. low']),
                'close': float(values['4. close']),
            })
        except (KeyError, TypeError, ValueError):
            continue
    rows.sort(key=lambda row: row['moment'])
    return rows
