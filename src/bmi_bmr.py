# ============================================
# bmi_bmr.py - Health Analytics Module (M2)
# ============================================

def calculate_bmi(weight, height_cm):
    height_m = height_cm / 100
    bmi = weight / (height_m ** 2)
    return round(bmi, 2)

def get_bmi_status(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"

def get_bmi_color(bmi):
    if bmi < 18.5:
        return "blue"
    elif bmi < 25:
        return "green"
    elif bmi < 30:
        return "orange"
    else:
        return "red"

def calculate_bmr(weight, height_cm, age, gender):
    if gender.lower() == "male":
        bmr = 10 * weight + 6.25 * height_cm - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height_cm - 5 * age - 161
    return round(bmr, 2)

def calculate_tdee(bmr, activity_level):
    factors = {
        "sedentary":          1.2,
        "lightly_active":     1.375,
        "moderately_active":  1.55,
        "very_active":        1.725
    }
    factor = factors.get(activity_level, 1.2)
    return round(bmr * factor, 2)

def calculate_daily_target(tdee, goal, stress, lifestyle):
    goal_adj = {
        "lose":    -500,
        "gain":    400,
        "maintain": 0
    }
    stress_adj = {
        "low":    0,
        "medium": -100,
        "high":   -200
    }
    lifestyle_adj = {
        "healthy":   0,
        "moderate":  -50,
        "unhealthy": -150
    }
    target = tdee
    target += goal_adj.get(goal, 0)
    target += stress_adj.get(stress, 0)
    target += lifestyle_adj.get(lifestyle, 0)
    return round(target, 2)

def get_full_health_report(weight, height_cm, age, gender,
                            activity_level, goal, 
                            stress, lifestyle):
    bmi    = calculate_bmi(weight, height_cm)
    status = get_bmi_status(bmi)
    color  = get_bmi_color(bmi)
    bmr    = calculate_bmr(weight, height_cm, age, gender)
    tdee   = calculate_tdee(bmr, activity_level)
    target = calculate_daily_target(
                tdee, goal, stress, lifestyle)

    return {
        "bmi":          bmi,
        "bmi_status":   status,
        "bmi_color":    color,
        "bmr":          bmr,
        "tdee":         tdee,
        "daily_target": target,
        "goal":         goal,
        "stress":       stress,
        "lifestyle":    lifestyle
    }