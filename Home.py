import streamlit as st
import pandas as pd
import time
import os
import plotly.express as px

from api import get_price, get_price_chart_data
from logger import log_to_csv
from news import fetch_crypto_news
from auth import get_current_user

# Custom Style
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }
.stExpanderHeader { font-weight: 600 !important; background-color: #2b2b2b !important; color: #fff !important; padding: 8px; border-radius: 5px; }
.stMetric { font-size: 1.3rem !important; }
.stButton>button { background-color: #4CAF50; color: white; font-weight: 600; border-radius: 6px; padding: 6px 12px; }
.news-card { background-color: #1f1f1f; padding: 15px; border-radius: 10px; margin-bottom: 15px; }
.news-title { font-weight: 600; color: #fafafa; }
.news-desc { font-size: 14px; color: #d0d0d0; }
@media screen and (max-width: 768px) {
    .element-container:nth-child(1) {
        flex-direction: column !important;
    }
}
</style>
""",
    unsafe_allow_html=True,
)

# Page config
st.set_page_config(page_title="💹 Multi-Crypto Tracker", layout="wide")

# Authentication
user = get_current_user()
if not user:
    st.warning("🔒 Please login to access the dashboard.")
    st.stop()

st.title(f"💹 Multi-Crypto Tracker — Welcome {user}")

# Constants
COINS = {
    "Bitcoin": "bitcoin",
    "Ethereum": "ethereum",
    "Solana": "solana",
    "Dogecoin": "dogecoin",
    "Cardano": "cardano",
    "Polygon": "matic-network",
    "XRP": "ripple",
    "Shiba Inu": "shiba-inu",
}

TIME_MAP = {"1 Day": 1, "7 Days": 7, "30 Days": 30}


# Sound Alert
def play_browser_sound():
    st.markdown(
        """
    <audio autoplay>
        <source src="alert.mp3" type="audio/mpeg">
    </audio>
    """,
        unsafe_allow_html=True,
    )


# Cache pricing
@st.cache_data(ttl=30)
def fetch_price(coin_id):
    return get_price(coin_id)


# ✅ Sidebar Controls
with st.sidebar:
    st.header("⚙️ Tracker Settings")
    selected_names = st.multiselect(
        "💰 Select Coins", list(COINS.keys()), default=["Bitcoin"]
    )
    chart_range = st.selectbox("📈 Chart Range", list(TIME_MAP.keys()), index=0)
    auto_refresh = st.checkbox("🔁 Auto-refresh every 20 sec")

    # ✅ Tracking toggle
    if "tracking_paused" not in st.session_state:
        st.session_state.tracking_paused = False

    if st.session_state.tracking_paused:
        if st.button("▶️ Resume Tracking"):
            st.session_state.tracking_paused = False
            st.rerun()
        st.warning("🛑 Tracking is paused. Click resume to continue.")
        st.stop()
    else:
        if st.button("⏸️ Pause Tracking"):
            st.session_state.tracking_paused = True
            st.rerun()


# Layout
left, right = st.columns([3, 1])
total_gain_loss = 0

# LEFT: Main Dashboard
with left:
    for name in selected_names:
        coin_id = COINS[name]
        price = fetch_price(coin_id)
        old_price = st.session_state.get(f"{coin_id}_prev", None)
        st.session_state[f"{coin_id}_prev"] = price
        delta = (
            round(price - old_price, 2)
            if (price is not None and old_price is not None)
            else None
        )

        with st.expander(f"📊 {name} Dashboard", expanded=True):
            if price is None:
                st.error("❌ Failed to fetch price.")
                continue

            st.metric(
                label=f"💸 {name} Price",
                value=f"₹{price:,.2f}",
                delta=f"{'+' if delta and delta > 0 else ''}{delta}" if delta else None,
                delta_color="normal",
            )

            col1, col2 = st.columns(2)
            lower = col1.number_input(
                f"🔻 Lower Limit", min_value=0.0, value=0.0, key=f"low_{coin_id}"
            )
            upper = col2.number_input(
                f"🔺 Upper Limit", min_value=0.0, value=0.0, key=f"up_{coin_id}"
            )

            if lower > 0 and price < lower:
                play_browser_sound()
                st.warning(f"🔻 Below ₹{lower:,}")
            elif upper > 0 and price > upper:
                play_browser_sound()
                st.warning(f"🔺 Above ₹{upper:,}")
            else:
                st.success(f"✔ Stable ₹{price:,}")

            # Logging
            if st.checkbox(f"📝 Log {name}", key=f"log_{coin_id}"):
                log_to_csv(name, price, user)
                st.success("✅ Logged to CSV!")

            # Chart
            with st.expander("📈 Show Chart"):
                days = TIME_MAP[chart_range]
                df = get_price_chart_data(coin_id, days=days)
                if df is not None and not df.empty:
                    start_price = df["Price"].iloc[0]
                    change = round(price - start_price, 2)
                    total_gain_loss += change

                    fig = px.line(
                        df,
                        x="Timestamp",
                        y="Price",
                        title=f"{name} - Last {days} Day(s)",
                        template="plotly_dark",
                        height=300,
                    )
                    fig.update_layout(margin=dict(t=30, b=20))
                    st.plotly_chart(fig, use_container_width=True)

                    st.caption(f"📈 Sparkline change: ₹{change:+,.2f}")
                else:
                    st.error("⚠️ No chart data found.")

            # Download CSV
            with st.expander("📎 Download History"):
                if os.path.exists("prices.csv"):
                    df = pd.read_csv("prices.csv")
                    user_df = df[(df["Coin"] == name) & (df["User"] == user)]
                    if not user_df.empty:
                        st.download_button(
                            label="⬇️ Download CSV",
                            data=user_df.to_csv(index=False).encode("utf-8"),
                            file_name=f"{name}_{user}_log.csv",
                            mime="text/csv",
                        )
                    else:
                        st.info("ℹ️ No data for this coin.")
                else:
                    st.warning("⚠️ No log file found.")

            st.markdown("---")

    # Portfolio Total
    st.subheader("📊 Portfolio Overview")
    st.metric("📈 Total Gain/Loss", f"₹{total_gain_loss:+,.2f}")

# RIGHT: Crypto News
with right:
    st.subheader("📰 Crypto News")
    news_items = fetch_crypto_news()
    if news_items:
        for article in news_items:
            st.markdown(
                f"""
            <div class='news-card'>
                <div class='news-title'>🔹 {article["title"]}</div>
                <div class='news-desc'>
                    🕒 {article["publishedAt"]} —
                    <a href="{article["url"]}" target="_blank">{article["source"]["name"]}</a>
                    <p>{article["description"] or ""}</p>
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )
    else:
        st.warning("⚠️ News fetch failed.")

# Auto Refresh
if auto_refresh:
    time.sleep(20)
    st.rerun()
