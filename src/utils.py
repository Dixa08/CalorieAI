# ============================================
# utils.py - Shared Utilities
# ============================================

import hashlib
import streamlit as st
import pandas as pd
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import PRIMARY_COLOR, SECONDARY_COLOR, CALORIES_CSV

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_login():
    if "user_id" not in st.session_state:
        st.warning("⚠️ Please login first!")
        st.page_link("pages/1_Login.py", label="Go to Login")
        st.stop()

def show_sidebar_user():
    if "username" in st.session_state:
        st.sidebar.markdown("---")
        st.sidebar.markdown(f"👤 **{st.session_state.username}**")
        st.sidebar.markdown("---")
        if st.sidebar.button("🚪 Logout"):
            st.session_state.clear()
            st.rerun()

def load_food_database():
    try:
        df = pd.read_csv(CALORIES_CSV)
        return df
    except:
        return pd.DataFrame()

def get_food_info(food_name):
    df = load_food_database()
    if df.empty:
        return None
    row = df[df['food_name'] == food_name]
    if row.empty:
        return None
    return row.iloc[0].to_dict()

def inject_css():
    st.markdown(f"""
    <style>
        .stButton > button {{
            background-color: {PRIMARY_COLOR};
            color: white;
            border: none;
            border-radius: 8px;
            padding: 8px 20px;
            font-weight: bold;
        }}
        .stButton > button:hover {{
            background-color: {SECONDARY_COLOR};
            color: white;
        }}
        .metric-card {{
            background: #f8f9fa;
            border-left: 4px solid {PRIMARY_COLOR};
            padding: 15px;
            border-radius: 8px;
            margin: 5px 0;
        }}
        .success-card {{
            background: #d4edda;
            border-left: 4px solid {SECONDARY_COLOR};
            padding: 15px;
            border-radius: 8px;
        }}
        .alert-card {{
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            border-radius: 8px;
        }}
    </style>
    """, unsafe_allow_html=True)

def show_metric_card(title, value, unit=""):
    st.markdown(f"""
    <div class="metric-card">
        <h4 style="margin:0;color:#666">{title}</h4>
        <h2 style="margin:0;color:{PRIMARY_COLOR}">{value} 
        <span style="font-size:14px">{unit}</span></h2>
    </div>
    """, unsafe_allow_html=True)