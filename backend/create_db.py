import sqlite3
import bcrypt

def authenticate(email, password):
    conn = sqlite3.connect("backend/crowdcount.db")
    cursor = conn.cursor()

    cursor.execute("SELECT hashed_password, is_admin FROM user WHERE email=?", (email,))
    user = cursor.fetchone()
    conn.close()

    if user:
        hashed_password, is_admin = user
        if bcrypt.checkpw(password.encode(), hashed_password.encode()):
            return True, is_admin
    return False, False
