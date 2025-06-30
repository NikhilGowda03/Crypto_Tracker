# auth.py

import sqlite3
import streamlit as st

DB_PATH = "crypto_tracker.db"


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ✅ Register a new user
def register_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if username already exists
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        conn.close()
        return False, "❌ Username already exists."

    # Insert new user
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)", (username, password)
    )
    conn.commit()
    conn.close()
    return True, "✅ Registration successful!"


# ✅ Login user
def login_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM users WHERE username = ? AND password = ?", (username, password)
    )
    user = cursor.fetchone()
    conn.close()
    if user:
        st.session_state["logged_in"] = True
        st.session_state["user_id"] = user["id"]
        st.session_state["username"] = username
        return True, "✅ Login successful!"
    else:
        return False, "❌ Invalid username or password."


# ✅ Logout user
def logout_user():
    st.session_state.clear()


# ✅ Get current logged in user
def get_current_user():
    if "logged_in" in st.session_state and st.session_state["logged_in"]:
        return st.session_state["username"], st.session_state["user_id"]
    return st.session_state.get("user")
