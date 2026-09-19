from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

# from db import get_db_connection
from supabase_client import supabase
from emission_factors import calculate_emission
from suggestions import get_suggestions


app = Flask(__name__)
CORS(app, origins=[
    "http://localhost:5173",
    "http://localhost:5174",
    "https://carbon-monitor-qnyx.onrender.com"
])


# =========================
# HOME
# =========================

@app.route("/")
def home():
    return "Carbon Tracker Backend + MySQL Connected Successfully"


# =========================
# GET SUGGESTIONS
# =========================

@app.route("/suggestions/<category>", methods=["GET"])
def suggestions(category):
    result = get_suggestions(category)
    return jsonify({
        "category": category,
        "impact": result["impact"],
        "tips": result["tips"]
    }), 200


# =========================
# CALCULATE EMISSION
# =========================

@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.get_json()

    category = data.get("category")
    value = data.get("value")

    if not category or value is None:
        return jsonify({
            "error": "Category and value are required"
        }), 400

    try:
        value = float(value)
    except (ValueError, TypeError):
        return jsonify({
            "error": "Value must be a number"
        }), 400

    emission = calculate_emission(category, value)

    if emission is None:
        return jsonify({
            "error": "Invalid category"
        }), 400

    return jsonify({
        "category": category,
        "value": value,
        "emission": emission,
        "unit": "kg CO2e"
    })


# =========================
# ADD ACTIVITY
# =========================

# =========================
# ADD ACTIVITY - SUPABASE
# =========================

@app.route("/activities", methods=["POST"])
def add_activity():
    data = request.get_json()

    user_id = data.get("user_id")
    category = data.get("category")
    value = data.get("value")
    unit = data.get("unit")
    activity_date = data.get("activity_date")

    if not user_id or not category or value is None or not unit or not activity_date:
        return jsonify({
            "error": "All fields are required"
        }), 400

    try:
        value = float(value)
    except (ValueError, TypeError):
        return jsonify({
            "error": "Value must be a number"
        }), 400

    emission = calculate_emission(category, value)

    if emission is None:
        return jsonify({
            "error": "Invalid category"
        }), 400

    try:
        response = supabase.table("activities").insert({
            "user_id": user_id,
            "category": category,
            "value": value,
            "unit": unit,
            "emission": emission,
            "activity_date": activity_date
        }).execute()

        return jsonify({
            "message": "Activity added successfully",
            "emission": emission,
            "unit": "kg CO2e",
            "suggestions": get_suggestions(category)
        }), 201

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500
# =========================
# GET ACTIVITY HISTORY
# =========================

# =========================
# GET ACTIVITY HISTORY - SUPABASE
# =========================

@app.route("/activities/<int:user_id>", methods=["GET"])
def get_activities(user_id):

    try:
        response = supabase.table("activities") \
            .select("*") \
            .eq("user_id", user_id) \
            .order("activity_date", desc=True) \
            .execute()

        activities = response.data

        return jsonify({
            "activities": activities
        }), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

# =========================
# TOTAL EMISSION
# =========================

# =========================
# TOTAL EMISSION - SUPABASE
# =========================

@app.route("/total-emission/<int:user_id>", methods=["GET"])
def total_emission(user_id):

    try:
        response = supabase.table("activities") \
            .select("emission") \
            .eq("user_id", user_id) \
            .execute()

        activities = response.data

        total = sum(
            float(activity["emission"])
            for activity in activities
        )

        return jsonify({
            "user_id": user_id,
            "total_emission": round(total, 2),
            "unit": "kg CO2e"
        }), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

# =========================
# MONTHLY EMISSION
# =========================

# =========================
# MONTHLY EMISSION - SUPABASE
# =========================

@app.route("/monthly-emission/<int:user_id>", methods=["GET"])
def monthly_emission(user_id):

    try:
        response = supabase.table("activities") \
            .select("emission, activity_date") \
            .eq("user_id", user_id) \
            .order("activity_date") \
            .execute()

        activities = response.data

        monthly_totals = {}

        for activity in activities:
            date = activity["activity_date"]
            month = date[:7]

            emission = float(activity["emission"])

            if month in monthly_totals:
                monthly_totals[month] += emission
            else:
                monthly_totals[month] = emission

        monthly_data = [
            {
                "month": month,
                "total_emission": round(total, 2)
            }
            for month, total in sorted(monthly_totals.items())
        ]

        return jsonify({
            "user_id": user_id,
            "monthly_emission": monthly_data,
            "unit": "kg CO2e"
        }), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

# =========================
# REGISTER
# =========================

# =========================
# REGISTER - SUPABASE
# =========================

@app.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({
            "error": "All fields are required"
        }), 400

    try:
        # Check existing user
        response = supabase.table("users") \
            .select("id") \
            .eq("email", email) \
            .execute()

        if response.data:
            return jsonify({
                "error": "Email already registered"
            }), 409

        # Hash password
        hashed_password = generate_password_hash(password)

        # Insert user
        supabase.table("users").insert({
            "name": name,
            "email": email,
            "password": hashed_password
        }).execute()

        return jsonify({
            "message": "Registration successful"
        }), 201

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

# =========================
# LOGIN
# =========================
# =========================
# LOGIN - SUPABASE
# =========================

@app.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "error": "Email and password are required"
        }), 400

    try:
        # Find user by email
        response = supabase.table("users") \
            .select("id, name, email, password") \
            .eq("email", email) \
            .execute()

        user_data = response.data

        if not user_data:
            return jsonify({
                "error": "Invalid email or password"
            }), 401

        user = user_data[0]

        # Check password
        if not check_password_hash(user["password"], password):
            return jsonify({
                "error": "Invalid email or password"
            }), 401

        return jsonify({
            "message": "Login successful",
            "user_id": user["id"],
            "name": user["name"],
            "email": user["email"]
        }), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

# =========================
# ADD REDUCTION GOAL
# =========================

# =========================
# ADD REDUCTION GOAL - SUPABASE
# =========================

@app.route("/goals", methods=["POST"])
def add_goal():

    data = request.get_json()

    user_id = data.get("user_id")
    target_reduction = data.get("target_reduction")
    start_date = data.get("start_date")
    end_date = data.get("end_date")

    if not user_id or target_reduction is None or not start_date or not end_date:
        return jsonify({
            "error": "All fields are required"
        }), 400

    try:
        target_reduction = float(target_reduction)

        if target_reduction <= 0 or target_reduction > 100:
            return jsonify({
                "error": "Reduction target must be between 1 and 100"
            }), 400

    except (ValueError, TypeError):
        return jsonify({
            "error": "Target reduction must be a number"
        }), 400

    try:
        supabase.table("goals").insert({
            "user_id": user_id,
            "target_reduction": target_reduction,
            "start_date": start_date,
            "end_date": end_date
        }).execute()

        return jsonify({
            "message": "Reduction goal added successfully",
            "target_reduction": target_reduction,
            "start_date": start_date,
            "end_date": end_date
        }), 201

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# =========================
# GET USER GOALS
# =========================

# =========================
# GET USER GOALS - SUPABASE
# =========================

@app.route("/goals/<int:user_id>", methods=["GET"])
def get_goals(user_id):

    try:
        response = supabase.table("goals") \
            .select("*") \
            .eq("user_id", user_id) \
            .order("end_date", desc=True) \
            .execute()

        goals = response.data

        return jsonify({
            "goals": goals
        }), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500
if __name__ == "__main__":
    app.run(debug=True)