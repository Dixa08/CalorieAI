# ============================================
# 3_Food_Log.py - Food Logging Page (M3)
# ============================================

import streamlit as st
import sys
import os
import pandas as pd
import plotly.express as px

sys.path.append(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
from src.utils import (check_login, show_sidebar_user,
                       inject_css, load_food_database,
                       get_food_info)
from src.food_logger import (log_food, get_daily_log,
                              get_daily_total)
from src.recommender import check_alerts
from src.profile import get_profile

st.set_page_config(
    page_title="CalorieAI - Food Log",
    page_icon="🍽️",
    layout="wide"
)

check_login()
inject_css()
show_sidebar_user()

st.title("🍽️ Food Log")
st.markdown("---")

# Load profile
profile = get_profile(st.session_state.user_id)
daily_target = profile["daily_target"] if profile else 2000

# Load food database
df = load_food_database()
food_names = df["food_name"].tolist() if not df.empty else []

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("➕ Add Food")

    meal_type = st.selectbox(
        "Meal Type",
        ["Breakfast", "Lunch", "Dinner", "Snack"]
    )

    selected_food = st.selectbox(
        "Select Food",
        food_names
    )

    quantity = st.number_input(
        "Quantity (servings)",
        min_value=0.5,
        max_value=10.0,
        value=1.0,
        step=0.5
    )

    # Show nutrition info
    if selected_food:
        food_info = get_food_info(selected_food)
        if food_info:
            st.markdown("**Nutrition per serving:**")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Calories",
                      f"{food_info['calories']}")
            c2.metric("Carbs",
                      f"{food_info['carbs']}g")
            c3.metric("Protein",
                      f"{food_info['protein']}g")
            c4.metric("Fat",
                      f"{food_info['fat']}g")

            st.markdown(
                f"**Total for {quantity} serving(s):**")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Calories",
                f"{food_info['calories']*quantity:.0f}")
            c2.metric("Carbs",
                f"{food_info['carbs']*quantity:.0f}g")
            c3.metric("Protein",
                f"{food_info['protein']*quantity:.0f}g")
            c4.metric("Fat",
                f"{food_info['fat']*quantity:.0f}g")

    if st.button("➕ Add to Log",
                 use_container_width=True):
        if selected_food:
            food_info = get_food_info(selected_food)
            if food_info:
                success, msg = log_food(
                    st.session_state.user_id,
                    selected_food,
                    meal_type,
                    quantity,
                    food_info["calories"],
                    food_info["carbs"],
                    food_info["protein"],
                    food_info["fat"]
                )
                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

with col2:
    st.subheader("📊 Today's Summary")

    # Daily totals
    totals = get_daily_total(st.session_state.user_id)

    # Progress bar
    progress = min(totals["calories"] / daily_target, 1.0)
    color = ("green" if progress < 0.85
             else "orange" if progress < 1.15
             else "red")

    st.markdown(
        f"**Calories: {totals['calories']:.0f} / "
        f"{daily_target:.0f}**")
    st.progress(progress)

    # Macros
    c1, c2, c3 = st.columns(3)
    c1.metric("Carbs",   f"{totals['carbs']:.0f}g")
    c2.metric("Protein", f"{totals['protein']:.0f}g")
    c3.metric("Fat",     f"{totals['fat']:.0f}g")

    # Alerts
    stress = profile["stress_level"] if profile else "low"
    alerts = check_alerts(
        totals["calories"], daily_target, stress)

    for alert in alerts:
        if alert["type"] == "danger":
            st.error(
                f"{alert['icon']} {alert['message']}")
        else:
            st.warning(
                f"{alert['icon']} {alert['message']}")

st.markdown("---")
st.subheader("📋 Today's Food Log")

# Show log table
logs = get_daily_log(st.session_state.user_id)

if logs:
    log_df = pd.DataFrame(logs, columns=[
        "Food", "Meal", "Qty",
        "Calories", "Carbs",
        "Protein", "Fat", "Time"
    ])
    st.dataframe(log_df, use_container_width=True)

    # Meal chart
    meal_totals = log_df.groupby("Meal")[
        "Calories"].sum().reset_index()
    fig = px.bar(
        meal_totals,
        x="Meal",
        y="Calories",
        title="Calories by Meal Type",
        color="Meal",
        color_discrete_sequence=[
            "#FF6B35", "#2E8B57",
            "#4ECDC4", "#FFE66D"
        ]
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No food logged today. Add your first meal!")