# Currency Converter & Exchange Rate Dashboard

## Project Overview

The Currency Converter & Exchange Rate Dashboard is a Python application that converts currencies using real-time exchange rates from a free public API.

It also stores exchange rates locally using JSON files and supports offline conversion using previously cached data.

## Features

1. Real-time currency conversion.
2. Supports multiple international currencies.
3. Exchange rate dashboard.
4. Automatic JSON caching.
5. Offline conversion support.
6. Currency code validation.
7. Network timeout and error handling.
8. Two-decimal conversion results.

## Technologies Used

- Python 3
- urllib
- JSON
- Datetime
- Object-Oriented Programming
- REST API

## API Used

Open Exchange Rates API:

https://open.er-api.com/v6/latest/USD

The application uses the free public API without requiring an API key.

## Project Structure

CurrencyConverter/
- main.py
- currency_client.py
- cache/
  - exchange_rates.json
- README.md
- requirements.txt

## How to Run

1. Install Python 3.
2. Open the project in VS Code.
3. Open the terminal.
4. Run:

python main.py

## Main Menu

1. Convert Currency
2. View Exchange Rates
3. Refresh Exchange Rates
4. Exit

## Offline Functionality

The application saves the latest retrieved rates in a local JSON file.

When the internet connection is unavailable, it uses previously saved rates for the selected base currency.

## Error Handling

- Invalid currency codes
- Invalid amounts
- Network connection failures
- API errors
- Request timeouts
- Missing cached exchange rates

## Internship

CodeNova Python Programming Internship
Batch 02

## Author

Brunda VS