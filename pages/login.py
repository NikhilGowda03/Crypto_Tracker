import streamlit as st
from auth import login_user

st.set_page_config(page_title="Login | Crypto Tracker", layout="centered")
st.title("🔐 Login to Crypto Tracker")

# Initialize session state
if "user" not in st.session_state:
    st.session_state.user = None

# Login Form
with st.form("login_form"):
    username = st.text_input("👤 Username")
    password = st.text_input("🔑 Password", type="password")
    submit = st.form_submit_button("Login")

    if submit:
        if login_user(username, password):
            st.success("✅ Login successful!")
            st.session_state.user = username
            st.switch_page("home.py")  # Redirect to main app
        else:
            st.error("❌ Invalid username or password")
