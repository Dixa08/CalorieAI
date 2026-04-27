# ============================================
# 2_Profile.py - Profile Page (M4)
# ============================================

import streamlit as st
import sys
import os
import plotly.graph_objects as go

sys.path.append(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
from src.utils import check_login, show_sidebar_user, inject_css
from src.profile import save_profile, get_profile

st.set_page_config(
    page_title="CalorieAI - Profile",
    page_icon="👤",
    layout="wide"
)

check_login()
inject_css()
show_sidebar_user()

st.title("👤 My Profile")
st.markdown("---")

# Load existing profile
profile = get_profile(st.session_state.user_id)

# Pre-fill values
name     = profile["name"]             if profile else ""
age      = profile["age"]              if profile else 20
weight   = profile["weight"]           if profile else 60.0
height   = profile["height_cm"]        if profile else 165.0
gender   = profile["gender"]           if profile else "Male"
goal     = profile["goal"]             if profile else "maintain"
activity = profile["activity_level"]   if profile else "sedentary"
stress   = profile["stress_level"]     if profile else "low"
lifestyle= profile["lifestyle"]        if profile else "moderate"
workload = profile["physical_workload"]if profile else "desk_job"

col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 Personal Info")
    name     = st.text_input("Full Name", value=name)
    age      = st.number_input("Age", 
                min_value=10, max_value=80, value=age)
    weight   = st.number_input("Weight (kg)",
                min_value=20.0, max_value=200.0, value=weight)
    height   = st.number_input("Height (cm)",
                min_value=100.0, max_value=250.0, value=height)
    gender   = st.selectbox("Gender",
                ["Male", "Female"],
                index=0 if gender == "Male" else 1)

with col2:
    st.subheader("🎯 Diet Factors")
    goal     = st.selectbox("Goal",
                ["lose", "gain", "maintain"],
                index=["lose","gain","maintain"].index(goal))
    activity = st.selectbox("Activity Level",
                ["sedentary", "lightly_active",
                 "moderately_active", "very_active"],
                index=["sedentary","lightly_active",
                       "moderately_active",
                       "very_active"].index(activity))
    stress   = st.selectbox("Stress Level",
                ["low", "medium", "high"],
                index=["low","medium","high"].index(stress))
    lifestyle= st.selectbox("Lifestyle",
                ["healthy", "moderate", "unhealthy"],
                index=["healthy","moderate",
                       "unhealthy"].index(lifestyle))
    workload = st.selectbox("Physical Workload",
                ["desk_job", "field_work", "gym"],
                index=["desk_job","field_work",
                       "gym"].index(workload))

st.markdown("---")

if st.button("💾 Save Profile", use_container_width=True):
    if name:
        success, result = save_profile(
            st.session_state.user_id,
            name, age, weight, height,
            gender, goal, activity,
            stress, lifestyle, workload
        )
        if success:
            st.success("✅ Profile saved!")
            st.session_state.profile = result

            # Show results
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("BMI", result["bmi"],
                          result["bmi_status"])
            with col2:
                st.metric("BMR", 
                          f"{result['bmr']} cal")
            with col3:
                st.metric("TDEE",
                          f"{result['tdee']} cal")
            with col4:
                st.metric("Daily Target",
                          f"{result['daily_target']} cal")

            # BMI Gauge
            bmi_colors = {
                "Underweight": "blue",
                "Normal":      "green",
                "Overweight":  "orange",
                "Obese":       "red"
            }
            color = bmi_colors.get(
                result["bmi_status"], "gray")

            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=result["bmi"],
                title={"text": f"BMI — {result['bmi_status']}"},
                gauge={
                    "axis": {"range": [10, 40]},
                    "bar":  {"color": color},
                    "steps": [
                        {"range": [10, 18.5],
                         "color": "#AED6F1"},
                        {"range": [18.5, 25],
                         "color": "#A9DFBF"},
                        {"range": [25, 30],
                         "color": "#FAD7A0"},
                        {"range": [30, 40],
                         "color": "#F1948A"},
                    ]
                }
            ))
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error(f"❌ Error: {result}")
    else:
        st.warning("⚠️ Please enter your name!")