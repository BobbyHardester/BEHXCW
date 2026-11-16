import os
from datetime import datetime
from flask import Flask, render_template, request, flash

from stocks import load_symbols
from alpha_vantage import TIME_SERIES, fetch_time_series, filter_by_date, ApiError
from charts import CHART_TYPES, build_chart

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "your secret key"


def parse_date(text):
    try:
        return datetime.strptime(text, '%Y-%m-%d').date()
    except (TypeError, ValueError):
        return None


def validate_form(form, symbols):
    errors = []
    symbol = form.get('symbol', '').strip().upper()
    chart_type = form.get('chart_type', '').strip()
    time_series = form.get('time_series', '').strip()
    start_date = parse_date(form.get('start_date', '').strip())
    end_date = parse_date(form.get('end_date', '').strip())

    if not symbol:
        errors.append('Symbol is required!')
    elif symbol not in symbols:
        errors.append('Symbol must be chosen from the list!')

    if not chart_type:
        errors.append('Chart type is required!')
    elif chart_type not in CHART_TYPES:
        errors.append('Chart type must be 1 (Bar) or 2 (Line)!')

    if not time_series:
        errors.append('Time series is required!')
    elif time_series not in TIME_SERIES:
        errors.append('Time series must be chosen from the list!')

    if not form.get('start_date', '').strip():
        errors.append('Start date is required!')
    elif start_date is None:
        errors.append('Start date must be a real date in YYYY-MM-DD format!')

    if not form.get('end_date', '').strip():
        errors.append('End date is required!')
    elif end_date is None:
        errors.append('End date must be a real date in YYYY-MM-DD format!')

    if start_date and end_date and end_date < start_date:
        errors.append('End date cannot be before the start date!')

    return errors, symbol, chart_type, time_series, start_date, end_date


@app.route('/', methods=('GET', 'POST'))
def index():
    stocks = load_symbols()
    symbols = [stock['symbol'] for stock in stocks]
    chart = None

    if request.method == 'POST':
        errors, symbol, chart_type, time_series, start_date, end_date = validate_form(request.form, symbols)
        if errors:
            for error in errors:
                flash(error)
        else:
            try:
                api_key = os.environ.get('ALPHA_VANTAGE_API_KEY', 'demo')
                data = fetch_time_series(symbol, time_series, api_key)
                rows = filter_by_date(data, start_date, end_date)
                if not rows:
                    flash('No data was found for {} between {} and {}.'.format(symbol, start_date, end_date))
                else:
                    chart = build_chart(symbol, chart_type, rows, start_date, end_date)
            except ApiError as error:
                flash(str(error))
            except Exception:
                flash('Something went wrong while creating the chart. Please try again.')

    return render_template(
        'index.html',
        stocks=stocks,
        chart_types=CHART_TYPES,
        time_series=TIME_SERIES,
        form=request.form,
        chart=chart,
    )


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
