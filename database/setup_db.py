import sqlite3

def create_database():
    conn = sqlite3.connect("sustainable_farming.db")
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS farmer_advice (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        farm_id TEXT,
        soil_pH REAL,
        soil_moisture REAL,
        temperature REAL,
        rainfall REAL,
        crop_type TEXT,
        fertilizer_usage REAL,
        pesticide_usage REAL,
        crop_yield REAL,
        sustainability_score REAL,
        recommendation TEXT
    );
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS market_trends (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        market_id TEXT,
        product TEXT,
        market_price REAL,
        demand_index REAL,
        supply_index REAL,
        competitor_price REAL,
        economic_indicator REAL,
        weather_impact REAL,
        seasonal_factor REAL,
        consumer_trend REAL,
        recommendation TEXT
    );
    """)
        
    # Use the original structure for recommendations table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recommendations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        prompt TEXT,
        farm_advice TEXT,
        market_advice TEXT
    );
    """)
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
    print("Database setup complete!")