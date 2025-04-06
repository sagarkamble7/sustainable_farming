import sqlite3

def save_recommendation(prompt, farm_advice, market_advice):
    """
    Save the recommendation to the database
    """
    conn = sqlite3.connect("sustainable_farming.db")
    cursor = conn.cursor()
    
    # Create the recommendations table if it doesn't exist (using original structure)
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
    """Get all saved recommendations"""
    conn = sqlite3.connect("sustainable_farming.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM recommendations")
    data = cursor.fetchall()
    
    conn.close()
    return data

def get_recommendation_summary():
    """Return a simplified summary of past recommendations for display in a table"""
    conn = sqlite3.connect("sustainable_farming.db")
    cursor = conn.cursor()
    
    # Use the original query that works with your existing structure
    cursor.execute("""
        SELECT 
            id,
            substr(prompt, 1, 50) || CASE WHEN length(prompt) > 50 THEN '...' ELSE '' END as short_prompt,
            substr(farm_advice, 1, 75) || CASE WHEN length(farm_advice) > 75 THEN '...' ELSE '' END as short_farm_advice,
            substr(market_advice, 1, 75) || CASE WHEN length(market_advice) > 75 THEN '...' ELSE '' END as short_market_advice
        FROM recommendations
    """)
    data = cursor.fetchall()
    
    conn.close()
    return data

def extract_key_metrics(text):
    """
    Extract key farming metrics from text like pH, moisture, temperature, etc.
    Returns a bulleted list with just the important data points
    """
    metrics = []
    key_phrases = [
        "pH", "moisture", "temperature", "rainfall", "fertilizer", 
        "yield", "price", "demand", "market", "crop", "soil"
    ]
    
    sentences = text.split('. ')
    for sentence in sentences:
        for phrase in key_phrases:
            if phrase.lower() in sentence.lower():
                # Clean up the sentence a bit
                clean_sentence = sentence.strip()
                if not clean_sentence.endswith('.'):
                    clean_sentence += '.'
                metrics.append(clean_sentence)
                break
    
    # Return the first 3 key metrics, or a summary if none found
    if metrics:
        return "; ".join(metrics[:3]) + "..."
    else:
        return text[:75] + ("..." if len(text) > 75 else "")

def get_recommendation_by_id(recommendation_id):
    """Get a full recommendation by its ID"""
    conn = sqlite3.connect("sustainable_farming.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM recommendations WHERE id = ?", (recommendation_id,))
    data = cursor.fetchone()
    
    conn.close()
    return data