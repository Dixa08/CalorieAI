import streamlit as st
from database.init_db import init_users_db, init_food_logs_db

init_users_db()
init_food_logs_db()

st.set_page_config(
    page_title="CalorieAI",
    page_icon="🥗",
    layout="wide"
)

st.markdown("""
<div style='text-align:center;padding:40px'>
    <h1 style='color:#FF6B35'>🥗 CalorieAI</h1>
    <h3 style='color:#666'>Smart Dietary Tracking 
    for Indian Students</h3>
    <p style='color:#888'>Using MobileNetV2 Deep Learning 
    — 87% Accuracy on Indian Food</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
col1,col2,col3 = st.columns(3)
col1.info("🔐 Login to get started")
col2.info("📸 Scan food with AI camera")
col3.info("📊 Track your daily nutrition")