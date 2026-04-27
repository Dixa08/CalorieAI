# ============================================
# food_logger.py - Food Logging Module (M3)
# ============================================

import sqlite3
import datetime
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import FOOD_LOG_DB

def log_food(user_id, food_name, meal_type,
             quantity, calories, carbs, protein, fat):
    try:
        conn = sqlite3.connect(FOOD_LOG_DB)
        c = conn.cursor()
        now = datetime.datetime.now()
        c.execute("""
            INSERT INTO food_log
            (user_id, food_name, meal_type, quantity,
             calories, carbs, protein, fat,
             log_date, log_time)
            VALUES (?,?,?,?,?,?,?,?,?,?)
        """, (
            user_id, food_name, meal_type, quantity,
            round(calories * quantity, 2),
            round(carbs * quantity, 2),
            round(protein * quantity, 2),
            round(fat * quantity, 2),
            now.strftime("%Y-%m-%d"),
            now.strftime("%H:%M:%S")
        ))
        conn.commit()
        conn.close()
        return True, f"✅ {food_name} logged!"
    except Exception as e:
        return False, f"❌ Error: {str(e)}"

def get_daily_log(user_id, date=None):
    if date is None:
        date = datetime.datetime.now().strftime("%Y-%m-%d")
    try:
        conn = sqlite3.connect(FOOD_LOG_DB)
        c = conn.cursor()
        c.execute("""
            SELECT food_name, meal_type, quantity,
                   calories, carbs, protein, fat, log_time
            FROM food_log
            WHERE user_id=? AND log_date=?
            ORDER BY log_time
        """, (user_id, date))
        logs = c.fetchall()
        conn.close()
        return logs
    except:
        return []

def get_daily_total(user_id, date=None):
    if date is None:
        date = datetime.datetime.now().strftime("%Y-%m-%d")
    try:
        conn = sqlite3.connect(FOOD_LOG_DB)
        c = conn.cursor()
        c.execute("""
            SELECT SUM(calories), SUM(carbs),
                   SUM(protein), SUM(fat)
            FROM food_log
            WHERE user_id=? AND log_date=?
        """, (user_id, date))
        result = c.fetchone()
        conn.close()
        return {
            "calories": round(result[0] or 0, 2),
            "carbs":    round(result[1] or 0, 2),
            "protein":  round(result[2] or 0, 2),
            "fat":      round(result[3] or 0, 2)
        }
    except:
        return {
            "calories": 0,
            "carbs":    0,
            "protein":  0,
            "fat":      0
        }

def get_weekly_logs(user_id):
    try:
        conn = sqlite3.connect(FOOD_LOG_DB)
        c = conn.cursor()
        c.execute("""
            SELECT log_date, SUM(calories)
            FROM food_log
            WHERE user_id=?
            GROUP BY log_date
            ORDER BY log_date DESC
            LIMIT 7
        """, (user_id,))
        logs = c.fetchall()
        conn.close()
        return logs
    except:
        return []

def delete_log(log_id):
    try:
        conn = sqlite3.connect(FOOD_LOG_DB)
        c = conn.cursor()
        c.execute("DELETE FROM food_log WHERE id=?", 
                  (log_id,))
        conn.commit()
        conn.close()
        return True
    except:
        return False# ============================================
# predict_food.py - Food Recognition (M1)
# ============================================

import numpy as np
import os
import sys
from PIL import Image

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import IMAGE_SIZE, FOOD_CLASSES, MODEL_PATH

MODEL = None

def load_model():
    global MODEL
    if MODEL is not None:
        return MODEL
    try:
        import tensorflow as tf
        model_path = os.path.join(MODEL_PATH, 
                                  "mobilenetv2_food.keras")
        if not os.path.exists(model_path):
            print("❌ Model not found! Train model first.")
            return None
        MODEL = tf.keras.models.load_model(model_path)
        print("✅ MobileNetV2 model loaded!")
        return MODEL
    except Exception as e:
        print(f"❌ Error loading model: {str(e)}")
        return None

def preprocess_image(image):
    try:
        if isinstance(image, str):
            img = Image.open(image)
        else:
            img = Image.open(image)
        
        # Convert to RGB
        img = img.convert("RGB")
        
        # Resize to 224x224
        img = img.resize(IMAGE_SIZE)
        
        # Convert to numpy array
        img_array = np.array(img)
        
        # Normalize to [0, 1]
        img_array = img_array / 255.0
        
        # Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array
    except Exception as e:
        print(f"❌ Preprocessing error: {str(e)}")
        return None

def predict_food(image_file):
    try:
        # Load model
        model = load_model()
        if model is None:
            return {
                "success":    False,
                "error":      "Model not found. Please train model first.",
                "food":       None,
                "confidence": 0
            }

        # Preprocess image
        img_array = preprocess_image(image_file)
        if img_array is None:
            return {
                "success":    False,
                "error":      "Image preprocessing failed.",
                "food":       None,
                "confidence": 0
            }

        # Predict
        predictions = model.predict(img_array, verbose=0)
        predicted_index = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_index])
        predicted_food = FOOD_CLASSES[predicted_index]

        return {
            "success":    True,
            "food":       predicted_food,
            "confidence": round(confidence * 100, 2),
            "all_predictions": {
                FOOD_CLASSES[i]: round(float(predictions[0][i]) * 100, 2)
                for i in range(len(FOOD_CLASSES))
            }
        }

    except Exception as e:
        return {
            "success":    False,
            "error":      str(e),
            "food":       None,
            "confidence": 0
        }

def get_top_predictions(image_file, top_n=3):
    result = predict_food(image_file)
    if not result["success"]:
        return []
    
    all_preds = result["all_predictions"]
    sorted_preds = sorted(
        all_preds.items(),
        key=lambda x: x[1],
        reverse=True
    )
    return sorted_preds[:top_n]