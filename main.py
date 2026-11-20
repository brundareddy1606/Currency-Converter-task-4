from currency_client import CurrencyClient
from datetime import datetime

client = CurrencyClient()


def display_header():
    print("\n" + "=" * 55)
    print("          CURRENCY CONVERTER DASHBOARD")
    print("=" * 55)
    print("       Real-Time Exchange Rate System")
    print("=" * 55)


def display_menu():
    print("\n--------------- MAIN MENU ----------------")
    print("1. Convert Currency")
    print("2. View Exchange Rates")
    print("3. Refresh Exchange Rates")
    print("4. Exit")
    print("------------------------------------------")


def get_amount():

    while True:
        try:
            amount = float(input("Enter amount: "))

            if amount <= 0:
                print("Please enter an amount greater than zero.")
                continue

            return amount

        except ValueError:
            print("Invalid amount. Enter a valid number.")


def get_currency(prompt):

    while True:
        currency = input(prompt).strip().upper()

        try:
            return client.validate_currency(currency)

        except ValueError as error:
            print(error)


def convert_currency():

    print("\n========== CURRENCY CONVERSION ==========")

    amount = get_amount()

    from_currency = get_currency("From currency (e.g. USD): ")
    to_currency = get_currency("To currency (e.g. INR): ")

    try:
        result = client.convert(
            amount,
            from_currency,
            to_currency
        )

        print("\n" + "=" * 45)
        print("           CONVERSION RESULT")
        print("=" * 45)

        print(
            f"Original Amount : "
            f"{result['amount']:.2f} {result['from_currency']}"
        )

        print(
            f"Exchange Rate   : "
            f"1 {from_currency} = "
            f"{result['rate']:.6f} {to_currency}"
        )

        print(
            f"Converted Amount: "
            f"{result['converted_amount']:.2f} {to_currency}"
        )

        print(f"Data Source     : {result['mode']}")
        print(f"Last Updated    : {result['updated_time']}")

        print("=" * 45)

    except (ValueError, ConnectionError, KeyError) as error:
        print(f"\nError: {error}")


def view_exchange_rates():

    print("\n========== EXCHANGE RATE DASHBOARD ==========")

    base_currency = get_currency(
        "Enter base currency (e.g. USD): "
    )

    try:
        rates, updated_time, mode = client.show_rates(
            base_currency
        )

        print(f"\nBase Currency: {base_currency}")
        print(f"Data Source  : {mode}")
        print(f"Last Updated : {updated_time}")

        print("\n----------- AVAILABLE CURRENCIES -----------")

        for currency, rate in sorted(rates.items()):
            print(f"{base_currency} -> {currency}: {rate:.6f}")

        print("--------------------------------------------")

    except (ValueError, ConnectionError, KeyError) as error:
        print(f"\nError: {error}")


def refresh_rates():

    print("\n========== REFRESH EXCHANGE RATES ==========")

    base_currency = get_currency(
        "Enter base currency (e.g. USD): "
    )

    try:
        rates, updated_time = client.fetch_rates(base_currency)

        print("\nExchange rates refreshed successfully!")
        print(f"Base Currency : {base_currency}")
        print(f"Available Rates: {len(rates)}")
        print(f"Last Updated  : {updated_time}")
        print("Rates saved in local JSON cache.")

    except Exception as error:
        print(f"\nUnable to refresh rates: {error}")


def main():

    display_header()

    while True:

        display_menu()

        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            convert_currency()

        elif choice == "2":
            view_exchange_rates()

        elif choice == "3":
            refresh_rates()

        elif choice == "4":
            print("\nThank you for using Currency Converter!")
            print("Application closed successfully.")
            break

        else:
            print("\nInvalid choice. Please select 1, 2, 3 or 4.")


if __name__ == "__main__":
    main()