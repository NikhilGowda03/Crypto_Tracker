import time
import threading
from colorama import Fore, init
from api import get_price
from alert import play_beep, play_mp3_alert
from logger import log_to_csv, initialize_csv
from config import get_coin_choices

init(autoreset=True)
stop_tracking = False


def listen_for_stop():
    global stop_tracking
    while True:
        if input("👉 Press 'q' to stop tracking: ").strip().lower() == "q":
            stop_tracking = True
            break


def track_alert_range():
    global stop_tracking

    print("📊 Crypto Multi-Coin Price Tracker")
    selected_coins = get_coin_choices()

    if not selected_coins:
        print(Fore.RED + "❌ No valid selection. Exiting.")
        return

    coin_limits = {}
    for name, coin_id in selected_coins:
        price = get_price(coin_id)
        if price:
            print(Fore.YELLOW + f"Current {name} price: ₹{price:,}")
        else:
            print(Fore.RED + f"❌ Failed to fetch current price for {name}. Skipping.")
            continue

        try:
            lower = float(input(f"🔻 Lower limit for {name}: ₹"))
            upper = float(input(f"🔺 Upper limit for {name}: ₹"))
        except:
            print(Fore.RED + "❌ Invalid input. Skipping this coin.")
            continue

        print("Choose alert type:")
        print("1. 🔔 Beep")
        print("2. 🔊 MP3/WAV")
        sound_choice = input("Enter 1 or 2: ").strip()
        alert_fn = play_beep if sound_choice == "1" else play_mp3_alert

        coin_limits[coin_id] = {
            "name": name,
            "lower": lower,
            "upper": upper,
            "alert": alert_fn,
        }

    if not coin_limits:
        print(Fore.RED + "❌ No coins configured correctly.")
        return

    initialize_csv()

    print(Fore.GREEN + "\n🔁 Starting price tracking...\n")
    threading.Thread(target=listen_for_stop, daemon=True).start()

    while not stop_tracking:
        for coin_id, info in coin_limits.items():
            price = get_price(coin_id)
            if price:
                name = info["name"]
                lower = info["lower"]
                upper = info["upper"]
                alert_fn = info["alert"]
                price_str = f"₹{price:,}"
                log_to_csv(name, price)

                if price < lower:
                    alert_fn()
                    print(Fore.RED + f"🔻 {name} below ₹{lower:,} → {price_str}")
                elif price > upper:
                    alert_fn()
                    print(Fore.YELLOW + f"🔺 {name} above ₹{upper:,} → {price_str}")
                else:
                    print(Fore.GREEN + f"✔ {name} stable at {price_str}")
            else:
                print(Fore.RED + f"❌ Failed to fetch {coin_id}")
        time.sleep(30)

    print(Fore.CYAN + "\n✅ Tracking stopped. Goodbye!")


if __name__ == "__main__":
    track_alert_range()
