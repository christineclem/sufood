# Functions
from dotenv import load_dotenv
import os

import psycopg2

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def get_connection():
    connection = psycopg2.connect(DATABASE_URL)
    return connection

def dict_factory(cursor, row):
    fields = [x[0] for x in cursor.description]
    return {key:value for key, value in zip(fields, row)}

def get_all_customers():
    conn = get_connection()
    conn.row_factory = dict_factory
    cur = conn.cursor()

    cur.execute("SELECT * FROM customers WHERE deleted_at IS NULL")
    rows = cur.fetchall()

    conn.close()
     
    return rows

def insert_customer(data):
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("""
        INSERT INTO customers (name, email, phone, marketing, newsletter)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        data['name'],
        data['email'],
        data['phone'],
        data['marketing'],
        data['newsletter']
    ))

    conn.commit()
    conn.close()

def update_customer(update_data):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE customers
        SET name = %s, email = %s, phone = %s, marketing = %s, newsletter = %s
        WHERE id = %s
    """,
(
        update_data['name'],
        update_data['email'],
        update_data['phone'],
        update_data['marketing'],
        update_data['newsletter'],
        update_data['id']
    )
    )

    conn.commit()
    conn.close()