import os

# ============================================
# config.py - Global Settings for Whole Team
# ============================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "dataset")
TRAIN_PATH   = os.path.join(DATASET_PATH, "train")
VAL_PATH     = os.path.join(DATASET_PATH, "val")
TEST_PATH    = os.path.join(DATASET_PATH, "test")
MODEL_PATH   = os.path.join(BASE_DIR, "models")
DB_PATH      = os.path.join(BASE_DIR, "database")

# Model Settings
IMAGE_SIZE   = (224, 224)
BATCH_SIZE   = 32
EPOCHS       = 15
NUM_CLASSES  = 10

# Food Classes
FOOD_CLASSES = [
    "aloo_tikki",
    "biryani",
    "chapati",
    "dal_makhani",
    "dal_tadka",
    "kadai_paneer",
    "naan",
    "palak_paneer",
    "paneer_butter_masala",
    "poha"
]

# Diet Factors
ACTIVITY_FACTORS = {
    "sedentary":          1.2,
    "lightly_active":     1.375,
    "moderately_active":  1.55,
    "very_active":        1.725
}

STRESS_ADJUSTMENT = {
    "low":    0,
    "medium": -100,
    "high":   -200
}

LIFESTYLE_ADJUSTMENT = {
    "healthy":   0,
    "moderate":  -50,
    "unhealthy": -150
}

GOAL_ADJUSTMENT = {
    "lose":    -500,
    "gain":    +400,
    "maintain": 0
}

# Alert Thresholds
OVEREAT_THRESHOLD   = 1.15
UNDEREAT_THRESHOLD  = 0.75

# Database Paths
USERS_DB     = os.path.join(DB_PATH, "users.db")
FOOD_LOG_DB  = os.path.join(DB_PATH, "food_logs.db")
CALORIES_CSV = os.path.join(DB_PATH, "indian_food_calories.csv")

# UI Colors
PRIMARY_COLOR   = "#FF6B35"
SECONDARY_COLOR = "#2E8B57"