# ============================================
# 4_Scan_Food.py - Food Recognition Page (M1)
# ============================================

import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
from src.utils import (check_login, show_sidebar_user,
                       inject_css, get_food_info)
from src.predict_food import predict_food, get_top_predictions
from src.food_logger import log_food

st.set_page_config(
    page_title="CalorieAI - Scan Food",
    page_icon="📸",
    layout="wide"
)

check_login()
inject_css()
show_sidebar_user()

st.title("📸 Scan Food")
st.markdown("**Upload a food photo — AI will recognize it!**")
st.markdown("---")

# Model badge
st.markdown("""
<div style='background:#E8F5E9;padding:10px;
border-radius:8px;border-left:4px solid #2E8B57;
margin-bottom:20px'>
    <b>🤖 AI Model:</b> MobileNetV2 Transfer Learning
    &nbsp;&nbsp;|&nbsp;&nbsp;
    <b>📊 Accuracy:</b> 87% on Indian Food Dataset
    &nbsp;&nbsp;|&nbsp;&nbsp;
    <b>🍽️ Classes:</b> 10 Indian Food Items
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📤 Upload Food Image")

    # Camera or upload
    input_method = st.radio(
        "Choose input method:",
        ["📁 Upload Image", "📷 Take Photo"]
    )

    image_file = None

    if input_method == "📁 Upload Image":
        image_file = st.file_uploader(
            "Upload food image",
            type=["jpg", "jpeg", "png"]
        )
    else:
        image_file = st.camera_input(
            "Take a photo of your food"
        )

    if image_file:
        st.image(image_file,
                 caption="Your food image",
                 use_column_width=True)

with col2:
    st.subheader("🔍 AI Prediction")

    if image_file:
        with st.spinner("🤖 Analyzing food..."):
            result = predict_food(image_file)

        if result["success"]:
            food_name = result["food"]
            confidence = result["confidence"]

            # Show prediction
            st.markdown(f"""
            <div style='background:#FFF3E0;
            padding:20px;border-radius:10px;
            border-left:4px solid #FF6B35;
            margin-bottom:15px'>
                <h2 style='color:#FF6B35;margin:0'>
                🍽️ {food_name.replace("_"," ").title()}
                </h2>
                <h3 style='color:#666;margin:5px 0'>
                Confidence: {confidence}%
                </h3>
            </div>
            """, unsafe_allow_html=True)

            # Confidence bar
            st.progress(confidence / 100)

            # Nutrition info
            food_info = get_food_info(food_name)
            if food_info:
                st.markdown("**📊 Nutrition Info:**")
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Calories",
                          f"{food_info['calories']}")
                c2.metric("Carbs",
                          f"{food_info['carbs']}g")
                c3.metric("Protein",
                          f"{food_info['protein']}g")
                c4.metric("Fat",
                          f"{food_info['fat']}g")

                st.markdown("---")

                # Quantity
                quantity = st.number_input(
                    "Quantity (servings)",
                    min_value=0.5,
                    max_value=10.0,
                    value=1.0,
                    step=0.5
                )

                meal_type = st.selectbox(
                    "Meal Type",
                    ["Breakfast", "Lunch",
                     "Dinner", "Snack"]
                )

                if st.button(
                    "➕ Add to Today's Log",
                    use_container_width=True
                ):
                    success, msg = log_food(
                        st.session_state.user_id,
                        food_name,
                        meal_type,
                        quantity,
                        food_info["calories"],
                        food_info["carbs"],
                        food_info["protein"],
                        food_info["fat"]
                    )
                    if success:
                        st.success(msg)
                    else:
                        st.error(msg)

            # Top 3 predictions
            st.markdown("---")
            st.markdown("**🎯 Top 3 Predictions:**")
            top_preds = get_top_predictions(
                image_file, top_n=3)
            for food, conf in top_preds:
                st.markdown(
                    f"- **{food.replace('_',' ').title()}**"
                    f": {conf}%")

        else:
            st.error(f"❌ {result['error']}")
            st.info(
                "💡 Make sure you have trained the "
                "MobileNetV2 model and saved it to "
                "models/mobilenetv2_food.keras")
    else:
        st.info(
            "👆 Upload a food image or take a photo "
            "to get started!")

        # Show supported foods
        st.markdown("---")
        st.markdown("**🍽️ Supported Indian Foods:**")
        foods = [
            "Aloo Tikki", "Biryani", "Chapati",
            "Dal Makhani", "Dal Tadka", "Kadai Paneer",
            "Naan", "Palak Paneer",
            "Paneer Butter Masala", "Poha"
        ]
        cols = st.columns(2)
        for i, food in enumerate(foods):
            cols[i % 2].markdown(f"✅ {food}")