from flask import Blueprint, request, jsonify
from database.db import get_connection
import bcrypt
import uuid

auth_routes = Blueprint("auth_routes", __name__)


# ==============================
# SIGNUP
# ==============================

@auth_routes.route("/signup", methods=["POST"])
def signup():

    data = request.json

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role","staff")
    if not name or not email or not password:
        return jsonify({
            "success": False,
            "message": "All fields are required"
        }), 400

    conn = get_connection()
    cursor = conn.cursor()

    # check if user exists
    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()

    if user:
        return jsonify({
            "success": False,
            "message": "Email already registered"
        }), 400

    # hash password
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    cursor.execute("""
        INSERT INTO users (name,email,password,role)
        VALUES (%s,%s,%s,%s)
        """,(name,email,hashed_password,role))

    conn.commit()

    return jsonify({
        "success": True,
        "message": "Account created successfully"
    })


# ==============================
# LOGIN
# ==============================

@auth_routes.route("/login", methods=["POST"])
def login():

    data = request.json

    email = data.get("email")
    password = data.get("password")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()

    if not user:
        return jsonify({
            "success": False,
            "message": "User not found"
        }), 404

    stored_password = user["password"]

    if bcrypt.checkpw(password.encode("utf-8"), stored_password.encode("utf-8")):

        return jsonify({
            "success": True,
            "message": "Login successful",
            "user": {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"],
                "role": user["role"]
            }
        })

    else:
        return jsonify({
            "success": False,
            "message": "Invalid password"
        }), 401


# ==============================
# FORGOT PASSWORD
# ==============================

@auth_routes.route("/forgot-password", methods=["POST"])
def forgot_password():

    data = request.json
    email = data.get("email")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()

    if not user:
        return jsonify({
            "success": False,
            "message": "Email not found"
        })

    reset_token = str(uuid.uuid4())

    cursor.execute("""
        UPDATE users
        SET reset_token=%s
        WHERE email=%s
    """, (reset_token, email))

    conn.commit()

    return jsonify({
        "success": True,
        "message": "Reset token generated",
        "token": reset_token
    })


# ==============================
# RESET PASSWORD
# ==============================

@auth_routes.route("/reset-password", methods=["POST"])
def reset_password():

    data = request.json

    token = data.get("token")
    new_password = data.get("password")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE reset_token=%s", (token,))
    user = cursor.fetchone()

    if not user:
        return jsonify({
            "success": False,
            "message": "Invalid token"
        })

    hashed_password = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt())

    cursor.execute("""
        UPDATE users
        SET password=%s, reset_token=NULL
        WHERE id=%s
    """, (hashed_password, user["id"]))

    conn.commit()

    return jsonify({
        "success": True,
        "message": "Password reset successfully"
    })