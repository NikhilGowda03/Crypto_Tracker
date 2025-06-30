import platform
import winsound
from playsound import playsound
from colorama import Fore


def play_beep():
    if platform.system() == "Windows":
        winsound.Beep(1000, 500)


def play_mp3_alert():
    try:
        playsound("alert.mp3")
    except:
        print(Fore.RED + "❌ Could not play MP3 alert.")


# alert.py


def check_price_alert(price, lower, upper):
    if price is None:
        return "❌ Price fetch failed", "red"
    if price < lower:
        return f"🔻 Price below ₹{lower:,}", "red"
    elif price > upper:
        return f"🔺 Price above ₹{upper:,}", "yellow"
    else:
        return f"✔ Price stable", "green"
