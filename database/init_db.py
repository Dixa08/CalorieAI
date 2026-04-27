# ============================================
# init_db.py - Database Initialization
# ============================================

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)))

def init_users_db():
    conn = sqlite3.connect(os.path.join(DB_PATH, "users.db"))
    c = conn.cursor()
    
    # Users table
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            username    TEXT UNIQUE NOT NULL,
            password    TEXT NOT NULL,
            email       TEXT,
            created_at  TEXT
        )
    """)
    
    # Profiles table
    c.execute("""
        CREATE TABLE IF NOT EXISTS profiles (
            id                INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id           INTEGER,
            name              TEXT,
            age               INTEGER,
            weight            REAL,
            height_cm         REAL,
            gender            TEXT,
            goal              TEXT,
            activity_level    TEXT,
            stress_level      TEXT,
            lifestyle         TEXT,
            physical_workload TEXT,
            bmi               REAL,
            bmr               REAL,
            tdee              REAL,
            daily_target      REAL,
            updated_at        TEXT
        )
    """)
    
    conn.commit()
    conn.close()
    print("✅ users.db initialized!")

def init_food_logs_db():
    conn = sqlite3.connect(os.path.join(DB_PATH, "food_logs.db"))
    c = conn.cursor()
    
    # Food log table
    c.execute("""
        CREATE TABLE IF NOT EXISTS food_log (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER,
            food_name   TEXT,
            meal_type   TEXT,
            quantity    REAL,
            calories    REAL,
            carbs       REAL,
            protein     REAL,
            fat         REAL,
            log_date    TEXT,
            log_time    TEXT
        )
    """)
    
    # Weekly summary table
    c.execute("""
        CREATE TABLE IF NOT EXISTS weekly_summary (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id         INTEGER,
            week_start      TEXT,
            total_calories  REAL,
            avg_calories    REAL,
            pattern         TEXT
        )
    """)
    
    conn.commit()
    conn.close()
    print("✅ food_logs.db initialized!")

if __name__ == "__main__":
    init_users_db()
    init_food_logs_db()
    print("✅ All databases ready!")