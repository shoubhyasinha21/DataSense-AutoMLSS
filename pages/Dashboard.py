import streamlit as st
import pandas as pd
import streamlit as st

if "user" not in st.session_state:
    st.error("Please login first.")
    st.stop()

user = st.session_state["user"]

# Only Admin can access
if not user.get("is_admin", False):
    st.error("🚫 Access Denied. Admin Only.")
    st.stop()


from components.styles import load_css
from utils.database import (
    get_all_users,
    total_users,
    total_logins,
    get_login_history,
    clear_login_history,
)

st.set_page_config(page_title="Dashboard", layout="wide")
load_css()

st.title("📊 User Dashboard")

col1, col2 = st.columns(2)

with col1:
    st.metric("Total Users", total_users())

with col2:
    st.metric("Total Logins", total_logins())

st.subheader("Login History")

login_history = get_login_history()

if login_history:
    login_df = pd.DataFrame(
        login_history,
        columns=["Email", "Login Time"],
    )
    st.dataframe(login_df, use_container_width=True)

    if st.button("🗑️ Delete Login History", key="delete_login_history"):
        clear_login_history()
        st.success("Login history deleted successfully.")
        st.rerun()
else:
    st.info("No login history found.")

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