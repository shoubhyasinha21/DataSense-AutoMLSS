import streamlit as st
from datetime import datetime, timedelta

from utils.database import create_user, login_user

SESSION_TIMEOUT_MINUTES = 60


def check_session_timeout():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state["logged_in"]:
        return

    if "last_activity" not in st.session_state:
        st.session_state["last_activity"] = datetime.now()
        return

    inactive_time = datetime.now() - st.session_state["last_activity"]

    if inactive_time > timedelta(minutes=SESSION_TIMEOUT_MINUTES):
        logout_user()
        st.warning("Session expired. Please login again.")
        st.stop()

    st.session_state["last_activity"] = datetime.now()


def logout_user():
    st.session_state["logged_in"] = False
    st.session_state["user"] = None

    if "last_activity" in st.session_state:
        del st.session_state["last_activity"]


def render_auth_suite():
    st.markdown("""
    <div style="
    max-width:520px;
    margin:auto;
    margin-top:60px;
    padding:35px;
    border-radius:28px;
    background:linear-gradient(135deg,#0f172a,#1e1b4b);
    border:1px solid rgba(255,255,255,0.12);
    box-shadow:0 25px 80px rgba(0,0,0,0.45);
    text-align:center;
    ">
        <h1 style="color:white;">🚀 DataSense AutoMLSS</h1>
        <p style="color:#cbd5e1;">Login or create your account</p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🔐 Login", "📝 Sign Up"])

    with tab1:
        st.subheader("Login")

        email = st.text_input("Email", key="login_email").strip().lower()
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login", width="stretch", key="login_button"):
            if not email or not password:
                st.error("Please enter email and password.")
                return

            user = login_user(email, password)

            if user:
                st.session_state["logged_in"] = True
                st.session_state["user"] = {
                    "id": user[0],
                    "name": user[1],
                    "email": user[2],
                    "plan": user[4],
                    "is_admin": bool(user[5]),
                }
                st.session_state["last_activity"] = datetime.now()

                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid email or password.")

    with tab2:
        st.subheader("Create Account")

        name = st.text_input("Full Name", key="signup_name").strip()
        email = st.text_input("Email", key="signup_email").strip().lower()
        password = st.text_input("Password", type="password", key="signup_password")
        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            key="signup_confirm_password"
        )

        if st.button("Create Account", width="stretch", key="signup_button"):
            if not name or not email or not password:
                st.error("Please fill all fields.")
                return

            if len(password) < 6:
                st.error("Password must be at least 6 characters.")
                return

            if password != confirm_password:
                st.error("Passwords do not match.")
                return

            try:
                create_user(
                    name=name,
                    email=email,
                    password=password,
                    is_admin=0
                )
                st.success("Account created successfully. Please login.")
            except Exception:
                st.error("This email already exists. Please login instead.")