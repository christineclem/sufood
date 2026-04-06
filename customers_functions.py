# Functions
import os

import psycopg2
import sqlite3

def get_connection():
    connection = sqlite3.connect("test_crm.db")
    return connection

# From YouTube tutorial: https://youtu.be/AQFsWwxW0hU?si=2Dv98QQj3ECGzGaW
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
    # '?' must be changed to '%s' in psycopg2
    cur.execute("""
        INSERT INTO customers (name, email, phone, marketing, newsletter)
        VALUES (?, ?, ?, ?, ?)
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
        SET name = ?, email = ?, phone = ?, marketing = ?, newsletter = ?
        WHERE id = ?
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