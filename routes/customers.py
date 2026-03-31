from datetime import datetime, timezone
from dotenv import load_dotenv
import os

import psycopg2

from flask import Blueprint, render_template

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
customers_bp = Blueprint('customers', __name__)

@customers_bp.route("/new_customer")
def new_customer():
    return render_template("test_form.html")

@customers_bp.route("/view_customers")
def view():
    connection = psycopg2.connect(DATABASE_URL)
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM customers")
    rows = cursor.fetchall()
    
    connection.close()
    
    return str(rows)