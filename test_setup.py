import sqlite3
import os
from pathlib import Path

script_dir = Path(__file__).parent
db_path = script_dir / "netflix.db"

print(f"Database path: {db_path}")
print(f"Database exists: {db_path.exists()}")

if db_path.exists():
    print(f"Database size: {db_path.stat().st_size} bytes")
    
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM netflix")
        count = cursor.fetchone()[0]
        print(f"Total records: {count}")
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"Tables: {tables}")
        
        if count > 0:
            cursor.execute("SELECT title, type FROM netflix LIMIT 3")
            samples = cursor.fetchall()
            print(f"\nSample records:")
            for row in samples:
                print(f"  - {row[0][:50]} ({row[1]})")
        
        conn.close()
        print("\n✓ Database is working correctly!")
    except Exception as e:
        print(f"✗ Error: {e}")
else:
    print("✗ Database not found - setup may have failed")

with open(str(script_dir / "setup_test_output.txt"), "w") as f:
    f.write("Test completed")
