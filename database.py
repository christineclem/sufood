from customers_functions import get_connection

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    # id INTERGER PRIMARY KEY -> SERIAL PRIMARY KEY (psycopg2)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        phone TEXT,
        marketing BOOLEAN DEFAULT FALSE,
        newsletter BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        deleted_at TIMESTAMP WITH TIME ZONE DEFAULT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        delivery TEXT,
        paid_in_full BOOLEAN DEFAULT FALSE,
        payment_method TEXT,
        payment_plan TEXT,
        FOREIGN KEY (customer_id) REFERENCES customers(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        price NUMERIC (10, 2),
        created_at TIMESTAMP,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS order_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER ,
        product_id INTEGER,
        quantity INTEGER,
        price_at_time NUMERIC (10, 2),
        FOREIGN KEY (order_id) REFERENCES orders(id),
        FOREIGN KEY (product_id) REFERENCES products(id)
    )
    """)

    conn.commit()
    conn.close()

def reset_customers():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DROP TABLE customers;")

    conn.commit()
    conn.close()