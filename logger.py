import csv
from datetime import datetime
import os


# ✅ Function to log coin price for a user
def log_to_csv(coin_name, price, user):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = "prices.csv"
    file_exists = os.path.isfile(filename)

    try:
        with open(filename, mode="a", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file)

            # Write header if file doesn't exist
            if not file_exists:
                writer.writerow(["Timestamp", "Coin", "Price", "User"])

            # Write the new row
            writer.writerow([timestamp, coin_name, price, user])

        print(f"✅ Logged to {filename}: {coin_name}, ₹{price}, user: {user}")

    except Exception as e:
        print(f"❌ Failed to write to {filename}: {e}")


# ✅ Optional: Use this once to create the CSV file with header
def initialize_csv():
    filename = "prices.csv"
    if not os.path.exists(filename):
        try:
            with open(filename, mode="w", newline="", encoding="utf-8-sig") as file:
                writer = csv.writer(file)
                writer.writerow(["Timestamp", "Coin", "Price", "User"])
            print(f"✅ Initialized {filename} with header.")
        except Exception as e:
            print(f"❌ Error initializing {filename}: {e}")
