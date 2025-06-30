coin_options = {
    "1": ("Bitcoin", "bitcoin"),
    "2": ("Ethereum", "ethereum"),
    "3": ("Solana", "solana"),
    "4": ("Dogecoin", "dogecoin"),
    "5": ("Cardano", "cardano"),
    "6": ("Polygon", "matic-network"),
    "7": ("XRP", "ripple"),
    "8": ("Shiba Inu", "shiba-inu"),
}


def get_coin_choices():
    print("💱 Choose cryptocurrencies to track (comma-separated):")
    for key, (name, _) in coin_options.items():
        print(f"{key}. {name}")
    choices = input("Enter your choices (e.g., 1,2,4): ").split(",")
    selected = []
    for ch in choices:
        ch = ch.strip()
        if ch in coin_options:
            name, coin_id = coin_options[ch]
            selected.append((name, coin_id))
    return selected
