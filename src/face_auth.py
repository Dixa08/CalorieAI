# ============================================
# face_auth.py - Face Recognition Module (M4)
# ============================================

import sqlite3
import os
import sys
import pickle
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import USERS_DB

def encode_face(image_path):
    try:
        import face_recognition
        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)
        if len(encodings) == 0:
            return None, "❌ No face found in image!"
        return encodings[0], "✅ Face encoded!"
    except Exception as e:
        return None, f"❌ Error: {str(e)}"

def save_face_encoding(user_id, encoding):
    try:
        conn = sqlite3.connect(USERS_DB)
        c = conn.cursor()
        
        # Check if face_encoding column exists
        c.execute("PRAGMA table_info(users)")
        columns = [col[1] for col in c.fetchall()]
        
        if "face_encoding" not in columns:
            c.execute("""
                ALTER TABLE users 
                ADD COLUMN face_encoding BLOB
            """)
        
        # Save encoding as blob
        encoding_blob = pickle.dumps(encoding)
        c.execute("""
            UPDATE users 
            SET face_encoding=? 
            WHERE id=?
        """, (encoding_blob, user_id))
        
        conn.commit()
        conn.close()
        return True, "✅ Face saved!"
    except Exception as e:
        return False, f"❌ Error: {str(e)}"

def face_login(image_path):
    try:
        import face_recognition
        
        # Load live face
        live_image = face_recognition.load_image_file(image_path)
        live_encodings = face_recognition.face_encodings(live_image)
        
        if len(live_encodings) == 0:
            return False, None, "❌ No face detected!"
        
        live_encoding = live_encodings[0]
        
        # Get all stored encodings
        conn = sqlite3.connect(USERS_DB)
        c = conn.cursor()
        c.execute("""
            SELECT id, username, face_encoding 
            FROM users 
            WHERE face_encoding IS NOT NULL
        """)
        users = c.fetchall()
        conn.close()
        
        if not users:
            return False, None, "❌ No face registered!"
        
        # Compare with stored encodings
        for user_id, username, encoding_blob in users:
            stored_encoding = pickle.loads(encoding_blob)
            results = face_recognition.compare_faces(
                [stored_encoding], live_encoding,
                tolerance=0.6
            )
            if results[0]:
                return True, user_id, username
        
        return False, None, "❌ Face not recognized!"
        
    except Exception as e:
        return False, None, f"❌ Error: {str(e)}"

def register_face(user_id, image_file):
    try:
        import face_recognition
        import tempfile
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=".jpg"
        ) as tmp:
            tmp.write(image_file.read())
            tmp_path = tmp.name
        
        # Encode face
        encoding, msg = encode_face(tmp_path)
        os.unlink(tmp_path)
        
        if encoding is None:
            return False, msg
        
        # Save encoding
        return save_face_encoding(user_id, encoding)
        
    except Exception as e:
        return False, f"❌ Error: {str(e)}"