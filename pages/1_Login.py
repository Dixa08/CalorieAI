# ============================================
# 1_Login.py - Login & Register Page (M4)
# ============================================

import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.init_db import init_users_db, init_food_logs_db
from src.profile import register_user, login_user
from src.utils import inject_css

# Initialize DB
init_users_db()
init_food_logs_db()

st.set_page_config(
    page_title="CalorieAI - Login",
    page_icon="🥗",
    layout="centered"
)

inject_css()

# Header
st.markdown("""
<div style='text-align:center; padding:20px'>
    <h1 style='color:#FF6B35'>🥗 CalorieAI</h1>
    <p style='color:#666; font-size:18px'>
    Smart Food Tracking for Indian Students</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Tabs
tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])

# Login Tab
with tab1:
    st.subheader("Welcome Back!")
    username = st.text_input(
        "Username", 
        placeholder="Enter username",
        key="login_username"
    )
    password = st.text_input(
        "Password",
        type="password",
        placeholder="Enter password",
        key="login_password"
    )

    if st.button("🔐 Login", use_container_width=True):
        if username and password:
            success, user_id, uname = login_user(
                username, password
            )
            if success:
                st.session_state.user_id   = user_id
                st.session_state.username  = uname
                st.success(f"✅ Welcome {uname}!")
                st.switch_page("pages/2_Profile.py")
            else:
                st.error("❌ Invalid username or password!")
        else:
            st.warning("⚠️ Please fill all fields!")

# Register Tab
with tab2:
    st.subheader("Create Account")
    new_username = st.text_input(
        "Username",
        placeholder="Choose username",
        key="reg_username"
    )
    new_email = st.text_input(
        "Email",
        placeholder="Enter email",
        key="reg_email"
    )
    new_password = st.text_input(
        "Password",
        type="password",
        placeholder="Choose password",
        key="reg_password"
    )
    confirm_password = st.text_input(
        "Confirm Password",
        type="password",
        placeholder="Confirm password",
        key="reg_confirm"
    )

    if st.button("📝 Register", use_container_width=True):
        if all([new_username, new_email,
                new_password, confirm_password]):
            if new_password != confirm_password:
                st.error("❌ Passwords do not match!")
            else:
                success, msg = register_user(
                    new_username, new_password, new_email
                )
                if success:
                    st.success(msg)
                    st.info("Please login now!")
                else:
                    st.error(msg)
        else:
            st.warning("⚠️ Please fill all fields!")