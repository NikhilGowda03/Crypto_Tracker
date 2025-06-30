import streamlit as st
from auth import register_user

st.set_page_config(page_title="Register | Crypto Tracker", layout="centered")
st.title("📝 Register for Crypto Tracker")

with st.form("register_form"):
    username = st.text_input("👤 Choose a Username")
    password = st.text_input("🔐 Create Password", type="password")
    confirm = st.text_input("✅ Confirm Password", type="password")
    submit = st.form_submit_button("Register")

    if submit:
        if not username or not password or not confirm:
            st.warning("⚠️ All fields are required.")
        elif password != confirm:
            st.warning("⚠️ Passwords do not match.")
        elif register_user(username, password):
            st.success("✅ Registered successfully. Please login.")
            st.info("👉 Go to the login page.")
        else:
            st.error("❌ Username already exists. Try another.")
