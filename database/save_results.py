import sqlite3

def save_recommendation(prompt, farm_advice, market_advice):
    conn = sqlite3.connect("sustainable_farming.db")
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recommendations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        prompt TEXT,
        farm_advice TEXT,
        market_advice TEXT
    );
    """)

    cursor.execute("""
    INSERT INTO recommendations (prompt, farm_advice, market_advice)
    VALUES (?, ?, ?)
    """, (prompt, farm_advice, market_advice))

    conn.commit()
    conn.close()

def get_saved_recommendations():
    conn = sqlite3.connect("sustainable_farming.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM recommendations")
    data = cursor.fetchall()

    conn.close()
    return data
