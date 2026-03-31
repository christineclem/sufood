from datetime import datetime, timezone
from dotenv import load_dotenv
import os

import psycopg

from flask import Blueprint, request, render_template

load_dotenv()
customers_bp = Blueprint('customers', __name__)

@customers_bp.route("/new_customer")
def new_customer():
    return render_template("test_form.html")

@customers_bp.route("/add_customer", methods=["POST"])
def add():
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    created_at = datetime.now(timezone.utc)

    conn = psycopg.connect(os.environ.get("DATABASE_URL"))
    cursor = conn.cursor()

    cursor.execute("INSERT INTO customers (name, email, phone, created_at) VALUES (%s, %s, %s, %s)",
                   (name, email, phone, created_at)
    )
    
    conn.commit()
    conn.close()
    
    return "Customer added!"

@customers_bp.route("/view_customers")
def view():
    conn = psycopg.connect(os.environ.get("DATABASE_URL"))
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM customers")
    rows = cursor.fetchall()
    
    conn.close()
    
    return str(rows)