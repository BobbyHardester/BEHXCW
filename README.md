# Stock Data Visualizer

A Flask web app that queries the Alpha Vantage API and draws a bar or line chart of stock prices for a date range. The app runs in a Docker container.

## Setting the API key

Copy `.env.example` to a file named `.env` and replace `yourkey` with an Alpha Vantage API key. The `.env` file is listed in `.gitignore` so it will not be committed. Without a key the app uses the Alpha Vantage `demo` key, which only returns data for IBM.

## Running the app

```
docker-compose up --build
```

Then open http://localhost:5000 in a browser. Stop the app with `Ctrl+C` and `docker-compose down`.

## Using the app

1. Choose a stock symbol. The list is loaded from `stocks.csv` when the page loads.
2. Choose a chart type: Bar or Line.
3. Choose a time series: Intraday, Daily, Weekly or Monthly.
4. Choose a start date and an end date. The end date cannot be before the start date.
5. Press Submit. The chart displays below the form.

Any input error is shown at the top of the page and the form keeps the values that were entered.

## Project layout

| File | Purpose |
| --- | --- |
| `app.py` | Flask route for GET and POST, form validation |
| `stocks.py` | Loads the stock symbols from `stocks.csv` |
| `alpha_vantage.py` | Builds the API request, checks for API errors, filters by date range |
| `charts.py` | Creates the bar or line chart with pygal |
| `templates/` | Base layout, form page and 404 page |
| `static/style.css` | Page styling |
| `Dockerfile` | Builds the image |
| `docker-compose.yml` | Launches the container on port 5000 |

## Notes

- The free Alpha Vantage tier allows 25 requests per day. The app shows the API message if the limit is reached.
- The intraday function only returns recent data, so choose a recent date range for it.
