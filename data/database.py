import sqlite3

def create_connection():
    conn = sqlite3.connect('data/contracts.db')
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS contracts (
                        id INTEGER PRIMARY KEY,
                        client_name TEXT NOT NULL,
                        vendor_name TEXT NOT NULL,
                        amount REAL NOT NULL,
                        description1 TEXT,
                        description2 TEXT,
                        created_at TEXT NOT NULL
                    )''')
    conn.commit()
    conn.close()

def insert_contract(client_name, vendor_name, amount, description1, description2, created_at):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO contracts (client_name, vendor_name, amount, description1, description2, created_at)
                      VALUES (?, ?, ?, ?, ?, ?)''', 
                   (client_name, vendor_name, amount, description1, description2, created_at))
    conn.commit()
    conn.close()

def get_contracts():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM contracts ORDER BY created_at DESC')
    contracts = cursor.fetchall()
    conn.close()
    return contracts

def get_contract_count():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM contracts')
    count = cursor.fetchone()[0]
    conn.close()
    return count

create_table()
