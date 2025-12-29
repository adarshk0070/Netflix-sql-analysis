#!/usr/bin/env python3
import sys
import os

# Change to script directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Write output to file
with open("output.log", "w") as log:
    sys.stdout = log
    sys.stderr = log
    
    try:
        import sqlite3
        from pathlib import Path
        
        db_path = Path("netflix.db")
        print(f"Database path: {db_path}")
        print(f"Database exists: {db_path.exists()}")
        
        if db_path.exists():
            print(f"Database size: {db_path.stat().st_size} bytes")
            
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM netflix")
            count = cursor.fetchone()[0]
            print(f"Total records: {count}")
            
            if count > 0:
                print("✓ Setup successful!")
            else:
                print("✗ Table is empty")
            
            conn.close()
        else:
            print("✗ Database file not created")
    except Exception as e:
        import traceback
        print(f"Error: {e}")
        traceback.print_exc()

# Reset stdout
sys.stdout = sys.__stdout__
sys.stderr = sys.__stderr__
print("Output written to output.log")
