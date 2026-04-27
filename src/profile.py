# ============================================
# profile.py - User Profile Module (M4)
# ============================================

import sqlite3
import hashlib
import datetime
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import USERS_DB
from src.bmi_bmr import get_full_health_report

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password, email):
    try:
        conn = sqlite3.connect(USERS_DB)
        c = conn.cursor()
        c.execute("""
            INSERT INTO users (username, password, email, created_at)
            VALUES (?, ?, ?, ?)
        """, (username, hash_password(password), email,
              datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        conn.close()
        return True, "✅ Registration successful!"
    except sqlite3.IntegrityError:
        return False, "❌ Username already exists!"
    except Exception as e:
        return False, f"❌ Error: {str(e)}"

def login_user(username, password):
    try:
        conn = sqlite3.connect(USERS_DB)
        c = conn.cursor()
        c.execute("""
            SELECT id, username FROM users
            WHERE username=? AND password=?
        """, (username, hash_password(password)))
        user = c.fetchone()
        conn.close()
        if user:
            return True, user[0], user[1]
        return False, None, None
    except Exception as e:
        return False, None, None

def save_profile(user_id, name, age, weight,
                 height_cm, gender, goal,
                 activity_level, stress_level,
                 lifestyle, physical_workload):
    report = get_full_health_report(
        weight, height_cm, age, gender,
        activity_level, goal,
        stress_level, lifestyle
    )
    try:
        conn = sqlite3.connect(USERS_DB)
        c = conn.cursor()
        c.execute("DELETE FROM profiles WHERE user_id=?", 
                  (user_id,))
        c.execute("""
            INSERT INTO profiles (
                user_id, name, age, weight, height_cm,
                gender, goal, activity_level, stress_level,
                lifestyle, physical_workload,
                bmi, bmr, tdee, daily_target, updated_at
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            user_id, name, age, weight, height_cm,
            gender, goal, activity_level, stress_level,
            lifestyle, physical_workload,
            report["bmi"], report["bmr"],
            report["tdee"], report["daily_target"],
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        conn.commit()
        conn.close()
        return True, report
    except Exception as e:
        return False, str(e)

def get_profile(user_id):
    try:
        conn = sqlite3.connect(USERS_DB)
        c = conn.cursor()
        c.execute("""
            SELECT * FROM profiles WHERE user_id=?
        """, (user_id,))
        profile = c.fetchone()
        conn.close()
        if profile:
            return {
                "user_id":          profile[1],
                "name":             profile[2],
                "age":              profile[3],
                "weight":           profile[4],
                "height_cm":        profile[5],
                "gender":           profile[6],
                "goal":             profile[7],
                "activity_level":   profile[8],
                "stress_level":     profile[9],
                "lifestyle":        profile[10],
                "physical_workload":profile[11],
                "bmi":              profile[12],
                "bmr":              profile[13],
                "tdee":             profile[14],
                "daily_target":     profile[15]
            }
        return None
    except:
        return None