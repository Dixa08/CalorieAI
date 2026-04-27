# ============================================
# recommender.py - Recommendation Module (M3)
# ============================================

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import OVEREAT_THRESHOLD, UNDEREAT_THRESHOLD

# Goal based food recommendations
RECOMMENDATIONS = {
    "lose": [
        {"food": "Dal Tadka",   "calories": 180, "reason": "High protein, low fat"},
        {"food": "Poha",        "calories": 250, "reason": "Light, easy to digest"},
        {"food": "Chapati",     "calories": 120, "reason": "Low calorie, filling"},
        {"food": "Idli",        "calories": 130, "reason": "Steamed, very low fat"},
        {"food": "Palak Paneer","calories": 240, "reason": "Iron rich, filling"},
    ],
    "gain": [
        {"food": "Biryani",             "calories": 450, "reason": "High calorie, energy dense"},
        {"food": "Paneer Butter Masala","calories": 280, "reason": "High protein and fat"},
        {"food": "Naan",                "calories": 270, "reason": "High carbs for energy"},
        {"food": "Aloo Paratha",        "calories": 260, "reason": "Carb rich, filling"},
        {"food": "Dal Makhani",         "calories": 220, "reason": "Protein and fat rich"},
    ],
    "maintain": [
        {"food": "Roti",        "calories": 100, "reason": "Balanced carbs"},
        {"food": "Rajma",       "calories": 220, "reason": "Protein rich, balanced"},
        {"food": "Kadai Paneer","calories": 260, "reason": "Balanced macros"},
        {"food": "Chole",       "calories": 210, "reason": "High fiber, balanced"},
        {"food": "Upma",        "calories": 230, "reason": "Balanced breakfast"},
    ]
}

def get_recommendations(goal):
    return RECOMMENDATIONS.get(goal, RECOMMENDATIONS["maintain"])

def check_alerts(consumed_calories, daily_target, stress_level):
    alerts = []

    if consumed_calories > daily_target * OVEREAT_THRESHOLD:
        alerts.append({
            "type":    "danger",
            "icon":    "🚨",
            "message": f"Overeating alert! You consumed "
                      f"{consumed_calories:.0f} cal vs "
                      f"target {daily_target:.0f} cal"
        })

    if consumed_calories < daily_target * UNDEREAT_THRESHOLD:
        alerts.append({
            "type":    "warning",
            "icon":    "⚠️",
            "message": f"Undereating alert! Only "
                      f"{consumed_calories:.0f} cal consumed. "
                      f"Target is {daily_target:.0f} cal"
        })

    if stress_level == "high" and \
       consumed_calories > daily_target:
        alerts.append({
            "type":    "warning",
            "icon":    "😰",
            "message": "Stress eating detected! "
                      "High stress + excess calories"
        })

    return alerts

def detect_pattern(weekly_logs, daily_target):
    if not weekly_logs:
        return "insufficient_data"

    avg = sum(cal for _, cal in weekly_logs) / len(weekly_logs)

    if avg > daily_target * OVEREAT_THRESHOLD:
        return "overeating"
    elif avg < daily_target * UNDEREAT_THRESHOLD:
        return "undereating"
    else:
        return "balanced"

def get_healthy_alternatives(food_name):
    alternatives = {
        "biryani":    ["Chapati + Dal", "Poha", "Idli"],
        "naan":       ["Chapati", "Roti", "Rice"],
        "maggi":      ["Upma", "Poha", "Idli"],
        "samosa":     ["Aloo Tikki", "Idli", "Poha"],
        "aloo_paratha":["Chapati", "Roti", "Dal Tadka"],
    }
    return alternatives.get(food_name.lower(), [])