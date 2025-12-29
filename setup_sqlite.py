#!/usr/bin/env python3
"""
Netflix SQL Project Setup Script
Imports CSV data into SQLite database and sets up the project
No external dependencies required except pandas (for CSV reading)
"""

import sqlite3
import csv
import os
import sys
from pathlib import Path

def create_connection(db_path):
    """Create a SQLite database connection"""
    try:
        conn = sqlite3.connect(db_path)
        print(f"✓ Connected to database: {db_path}")
        return conn
    except sqlite3.Error as e:
        print(f"✗ Error connecting to database: {e}")
        sys.exit(1)

def create_table(conn):
    """Create the netflix table schema"""
    create_table_sql = """
    DROP TABLE IF EXISTS netflix;
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
    );
    """
    try:
        cursor = conn.cursor()
        for statement in create_table_sql.split(';'):
            if statement.strip():
                cursor.execute(statement)
        conn.commit()
        print("✓ Table 'netflix' created successfully")
    except sqlite3.Error as e:
        print(f"✗ Error creating table: {e}")
        sys.exit(1)

def import_csv_data(conn, csv_path):
    """Import CSV data into the netflix table"""
    if not os.path.exists(csv_path):
        print(f"✗ CSV file not found: {csv_path}")
        sys.exit(1)
    
    try:
        cursor = conn.cursor()
        with open(csv_path, 'r', encoding='utf-8') as f:
            csv_reader = csv.reader(f)
            headers = next(csv_reader)  # Skip header
            
            insert_sql = """
            INSERT INTO netflix 
            (show_id, type, title, director, casts, country, date_added, release_year, rating, duration, listed_in, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            rows = list(csv_reader)
            cursor.executemany(insert_sql, rows)
            conn.commit()
            
            print(f"✓ Imported {len(rows)} records from CSV")
    except Exception as e:
        print(f"✗ Error importing CSV: {e}")
        sys.exit(1)

def verify_data(conn):
    """Verify the data was imported correctly"""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM netflix")
        count = cursor.fetchone()[0]
        print(f"✓ Data verification: {count} records in database")
        
        cursor.execute("SELECT * FROM netflix LIMIT 1")
        sample = cursor.fetchone()
        print(f"✓ Sample record retrieved successfully")
        
        return count > 0
    except sqlite3.Error as e:
        print(f"✗ Error verifying data: {e}")
        return False

def main():
    print("\n" + "="*60)
    print("Netflix SQL Project - SQLite Setup")
    print("="*60 + "\n")
    
    script_dir = Path(__file__).parent
    db_path = script_dir / "netflix.db"
    csv_path = script_dir / "netflix_titles.csv"
    
    print(f"Project directory: {script_dir}")
    print(f"Database path: {db_path}")
    print(f"CSV path: {csv_path}\n")
    
    # Remove existing database if it exists
    if db_path.exists():
        db_path.unlink()
        print("⊘ Existing database removed\n")
    
    # Create connection
    conn = create_connection(str(db_path))
    
    # Create table
    print("\nStep 1: Creating table schema...")
    create_table(conn)
    
    # Import data
    print("\nStep 2: Importing CSV data...")
    import_csv_data(conn, str(csv_path))
    
    # Verify
    print("\nStep 3: Verifying import...")
    if verify_data(conn):
        print("\n" + "="*60)
        print("✓ Setup Complete! Database ready for analysis")
        print("="*60)
        print("\nNext steps:")
        print("1. Run: python run_queries.py (to execute all 15 queries)")
        print("2. Or open: query_interface.py (for interactive query tool)")
        print("\n")
    else:
        print("✗ Data verification failed")
        sys.exit(1)
    
    conn.close()

if __name__ == "__main__":
    main()
