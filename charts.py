import pygal

CHART_TYPES = {
    '1': 'Bar',
    '2': 'Line',
}


def build_chart(symbol, chart_type, rows, start_date, end_date):
    if chart_type == '1':
        chart = pygal.Bar(x_label_rotation=45, height=500)
    else:
        chart = pygal.Line(x_label_rotation=45, height=500)

    chart.title = 'Stock Data for {}: {} to {}'.format(symbol, start_date, end_date)
    chart.x_labels = [row['label'] for row in rows]
    if len(rows) > 40:
        step = len(rows) // 20
        chart.x_labels_major = chart.x_labels[::step]
        chart.show_minor_x_labels = False
    chart.add('Open', [row['open'] for row in rows])
    chart.add('High', [row['high'] for row in rows])
    chart.add('Low', [row['low'] for row in rows])
    chart.add('Close', [row['close'] for row in rows])
    return chart.render_data_uri()
