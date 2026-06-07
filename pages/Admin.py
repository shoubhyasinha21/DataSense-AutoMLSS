import streamlit as st
import pandas as pd

from components.styles import load_css
from utils.database import (
    total_users,
    total_logins,
    total_premium_users,
    get_all_users,
    get_login_history,
    get_training_history,
)

st.set_page_config(page_title="Admin Dashboard", layout="wide")
load_css()

st.title("🛡️ Admin Dashboard")

if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.error("Please login first.")
    st.stop()

user = st.session_state.get("user")

if not user or not user.get("is_admin"):
    st.error("Access denied. Admin only.")
    st.stop()

st.success("Welcome Admin")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Users", total_users())

with col2:
    st.metric("Total Logins", total_logins())

with col3:
    st.metric("Premium Users", total_premium_users())

st.subheader("Registered Users")

users = get_all_users()

if users:
    users_df = pd.DataFrame(
        users,
        columns=[
            "ID",
            "Name",
            "Email",
            "Plan",
            "Is Admin",
            "Created At",
            "Last Login",
        ],
    )
    st.dataframe(users_df, use_container_width=True)
else:
    st.info("No users found.")

st.subheader("Login History")

login_history = get_login_history()

if login_history:
    login_df = pd.DataFrame(
        login_history,
        columns=["Email", "Login Time"],
    )
    st.dataframe(login_df, use_container_width=True)
else:
    st.info("No login history found.")

st.subheader("Training History")

training_history = get_training_history()

if training_history:
    training_df = pd.DataFrame(
        training_history,
        columns=[
            "Email",
            "Target Column",
            "Task Type",
            "Best Model",
            "Score",
            "Time",
        ],
    )
    st.dataframe(training_df, use_container_width=True)
else:
    st.info("No training history found.")