import json
import re
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime, timezone


class CurrencyClient:

    API_URL = "https://open.er-api.com/v6/latest/{}"
    CACHE_FILE = Path(__file__).parent / "cache" / "exchange_rates.json"

    def __init__(self):
        self.CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)

        if not self.CACHE_FILE.exists():
            self.CACHE_FILE.write_text("{}", encoding="utf-8")

    def validate_currency(self, currency):
        currency = currency.strip().upper()

        if not re.fullmatch(r"[A-Z]{3}", currency):
            raise ValueError(
                "Currency code must contain exactly 3 letters."
            )

        return currency

    def load_cache(self):
        try:
            with open(self.CACHE_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

                if isinstance(data, dict):
                    return data

        except (json.JSONDecodeError, OSError):
            pass

        return {}

    def save_cache(self, base_currency, rates, updated_time):
        cache = self.load_cache()

        cache[base_currency] = {
            "base_currency": base_currency,
            "rates": rates,
            "last_updated": updated_time
        }

        with open(self.CACHE_FILE, "w", encoding="utf-8") as file:
            json.dump(cache, file, indent=4)

    def fetch_rates(self, base_currency):

        base_currency = self.validate_currency(base_currency)

        url = self.API_URL.format(base_currency)

        request = urllib.request.Request(
            url,
            headers={"User-Agent": "CurrencyConverter/1.0"}
        )

        with urllib.request.urlopen(request, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))

        if data.get("result") != "success":
            raise ValueError(
                data.get("error-type", "Invalid currency or API response.")
            )

        rates = data.get("rates")

        if not isinstance(rates, dict) or not rates:
            raise ValueError("Exchange rates are unavailable.")

        updated_time = data.get("time_last_update_utc", "Unknown")

        self.save_cache(base_currency, rates, updated_time)

        return rates, updated_time

    def get_rates(self, base_currency):

        base_currency = self.validate_currency(base_currency)

        try:
            rates, updated_time = self.fetch_rates(base_currency)

            return rates, updated_time, "ONLINE"

        except (
            urllib.error.URLError,
            urllib.error.HTTPError,
            TimeoutError,
            OSError,
            ValueError,
            json.JSONDecodeError
        ) as error:

            print(f"\nNetwork/API notice: {error}")

            cache = self.load_cache()

            cached_data = cache.get(base_currency)

            if cached_data:
                print("Using previously saved exchange rates.")

                return (
                    cached_data["rates"],
                    cached_data.get("last_updated", "Unknown"),
                    "OFFLINE"
                )

            raise ConnectionError(
                "No internet connection and no cached rates available "
                f"for {base_currency}. Please connect to the internet first."
            )

    def convert(self, amount, from_currency, to_currency):

        from_currency = self.validate_currency(from_currency)
        to_currency = self.validate_currency(to_currency)

        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")

        rates, updated_time, mode = self.get_rates(from_currency)

        if to_currency not in rates:
            raise ValueError(
                f"{to_currency} is not supported by the exchange rate API."
            )

        rate = rates[to_currency]
        converted_amount = amount * float(rate)

        return {
            "amount": amount,
            "from_currency": from_currency,
            "to_currency": to_currency,
            "rate": float(rate),
            "converted_amount": converted_amount,
            "updated_time": updated_time,
            "mode": mode
        }

    def show_rates(self, base_currency):

        base_currency = self.validate_currency(base_currency)

        rates, updated_time, mode = self.get_rates(base_currency)

        return rates, updated_time, mode