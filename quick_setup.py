import sqlite3
import csv
import os
from pathlib import Path

print("\n" + "="*60)
print("Netflix SQL Project - SQLite Setup")
print("="*60 + "\n")

script_dir = Path(__file__).parent
db_path = script_dir / "netflix.db"
csv_path = script_dir / "netflix_titles.csv"

print(f"Project directory: {script_dir}")
print(f"Database: {db_path}")
print(f"CSV file: {csv_path}\n")

if db_path.exists():
    db_path.unlink()
    print("Existing database removed\n")

try:
    conn = sqlite3.connect(str(db_path))
    print("✓ Connected to database")
    
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS netflix")
    cursor.execute("""
    CREATE TABLE netflix (
        show_id TEXT,
        type TEXT,
        title TEXT,
        director TEXT,
        casts TEXT,
        country TEXT,
        date_added TEXT,
        release_year INTEGER,
        rating TEXT,
        duration TEXT,
        listed_in TEXT,
        description TEXT
    )
    """)
    conn.commit()
    print("✓ Table created\n")
    
    print("Importing CSV data...")
    with open(str(csv_path), 'r', encoding='utf-8') as f:
        csv_reader = csv.reader(f)
        headers = next(csv_reader)
        rows = list(csv_reader)
        
        insert_sql = """
        INSERT INTO netflix VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        cursor.executemany(insert_sql, rows)
        conn.commit()
        print(f"✓ Imported {len(rows)} records\n")
    
    cursor.execute("SELECT COUNT(*) FROM netflix")
    count = cursor.fetchone()[0]
    print(f"✓ Verification: {count} records in database")
    
    cursor.execute("SELECT * FROM netflix LIMIT 1")
    sample = cursor.fetchone()
    print(f"✓ Sample record retrieved\n")
    
    print("="*60)
    print("✓ Setup Complete! Database ready")
    print("="*60)
    print("\nNext: python run_queries.py\n")
    
    conn.close()
    
except Exception as e:
    print(f"✗ Error: {e}")
