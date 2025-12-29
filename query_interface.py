#!/usr/bin/env python3
"""
Netflix SQL Project - Interactive Query Interface
Provides a command-line interface to query the Netflix database
"""

import sqlite3
import sys
from pathlib import Path
from datetime import datetime

class NetflixQueryInterface:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.connect()
    
    def connect(self):
        """Connect to the database"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()
            print(f"✓ Connected to database: {self.db_path}")
        except sqlite3.Error as e:
            print(f"✗ Connection error: {e}")
            sys.exit(1)
    
    def execute_query(self, sql):
        """Execute a SQL query and return results"""
        try:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"✗ Query error: {e}")
            return None
    
    def display_results(self, results, limit=20):
        """Display query results in a formatted table"""
        if not results:
            print("No results returned")
            return
        
        # Get column names
        columns = [desc[0] for desc in self.cursor.description] if self.cursor.description else []
        
        if not columns:
            return
        
        # Calculate column widths
        col_widths = [max(len(col), 15) for col in columns]
        for row in results[:limit]:
            for i, col in enumerate(columns):
                col_widths[i] = max(col_widths[i], len(str(row[col]))[:50])
        
        # Print header
        header = " │ ".join(col.ljust(width) for col, width in zip(columns, col_widths))
        print("┌" + "┬".join("─" * (width + 2) for width in col_widths) + "┐")
        print("│ " + " │ ".join(col.ljust(width) for col, width in zip(columns, col_widths)) + " │")
        print("├" + "┼".join("─" * (width + 2) for width in col_widths) + "┤")
        
        # Print rows
        for idx, row in enumerate(results):
            if idx >= limit:
                print(f"... and {len(results) - limit} more rows")
                break
            
            values = [str(row[col])[:50] for col in columns]
            print("│ " + " │ ".join(val.ljust(width) for val, width in zip(values, col_widths)) + " │")
        
        print("└" + "┴".join("─" * (width + 2) for width in col_widths) + "┘")
        print(f"\nRows: {len(results)}\n")
    
    def show_menu(self):
        """Display the main menu"""
        print("\n" + "="*70)
        print("NETFLIX SQL PROJECT - INTERACTIVE QUERY INTERFACE")
        print("="*70)
        print("\nQuick Queries:")
        print("  1. Movies vs TV Shows count")
        print("  2. Most common ratings by type")
        print("  3. Movies from 2020")
        print("  4. Top 5 countries with most content")
        print("  5. Longest movie")
        print("  6. TV shows with 5+ seasons")
        print("  7. Documentaries")
        print("  8. Content without director")
        print("  9. Salman Khan appearances (last 10 years)")
        print("  10. Top 10 Indian actors")
        print("  11. Content by 'kill' or 'violence' keywords")
        print("  12. Search by keyword")
        print("  13. Custom SQL query")
        print("  0. Exit")
        print("="*70 + "\n")
    
    def run_quick_query(self, choice):
        """Run pre-defined quick queries"""
        queries = {
            '1': ("SELECT type, COUNT(*) as count FROM netflix GROUP BY type;",
                  "Movies vs TV Shows"),
            '2': ("""SELECT type, rating, COUNT(*) as count 
                    FROM netflix GROUP BY type, rating 
                    ORDER BY type, count DESC LIMIT 10;""",
                  "Most common ratings"),
            '3': ("SELECT title, type, release_year, rating FROM netflix WHERE release_year = 2020 LIMIT 20;",
                  "Movies from 2020"),
            '4': ("SELECT country, COUNT(*) as count FROM netflix WHERE country IS NOT NULL GROUP BY country ORDER BY count DESC LIMIT 5;",
                  "Top 5 countries"),
            '5': ("SELECT title, type, duration FROM netflix WHERE type = 'Movie' ORDER BY CAST(SUBSTR(duration, 1, INSTR(duration, ' ') - 1) AS INTEGER) DESC LIMIT 1;",
                  "Longest movie"),
            '6': ("SELECT title, duration FROM netflix WHERE type = 'TV Show' AND CAST(SUBSTR(duration, 1, INSTR(duration, ' ') - 1) AS INTEGER) > 5 ORDER BY CAST(SUBSTR(duration, 1, INSTR(duration, ' ') - 1) AS INTEGER) DESC LIMIT 20;",
                  "TV shows with 5+ seasons"),
            '7': ("SELECT title, type, rating FROM netflix WHERE listed_in LIKE '%Documentaries%' LIMIT 20;",
                  "Documentaries"),
            '8': ("SELECT title, type, release_year FROM netflix WHERE director IS NULL OR director = '' LIMIT 20;",
                  "Content without director"),
            '9': ("SELECT title, casts, release_year FROM netflix WHERE casts LIKE '%Salman Khan%' ORDER BY release_year DESC LIMIT 10;",
                  "Salman Khan appearances"),
            '10': ("SELECT COUNT(*) as appearances FROM netflix WHERE country LIKE '%India%' LIMIT 10;",
                   "Indian content count"),
            '11': ("""SELECT 
                      CASE WHEN description LIKE '%kill%' OR description LIKE '%violence%' 
                           OR description LIKE '%Kill%' OR description LIKE '%Violence%' 
                      THEN 'Bad' ELSE 'Good' END as category,
                      COUNT(*) as count
                      FROM netflix GROUP BY category;""",
                   "Content by keywords"),
        }
        
        if choice in queries:
            sql, title = queries[choice]
            print(f"\n► {title}")
            print("-" * 70)
            results = self.execute_query(sql)
            if results is not None:
                self.display_results(results)
        else:
            print("Invalid choice!")
    
    def run_custom_query(self):
        """Allow user to run custom SQL"""
        print("\nEnter your SQL query (type 'END' on a new line to execute):")
        print("Example: SELECT * FROM netflix WHERE type = 'Movie' LIMIT 5;")
        print("-" * 70)
        
        lines = []
        while True:
            line = input()
            if line.upper() == 'END':
                break
            lines.append(line)
        
        sql = "\n".join(lines)
        
        if sql.strip():
            print("\nExecuting query...")
            print("-" * 70)
            results = self.execute_query(sql)
            if results is not None:
                self.display_results(results)
    
    def search_by_keyword(self):
        """Search content by title or description keyword"""
        keyword = input("Enter search keyword: ").strip()
        
        if not keyword:
            print("No keyword provided!")
            return
        
        sql = f"""
        SELECT title, type, rating, listed_in 
        FROM netflix 
        WHERE title LIKE '%{keyword}%' 
           OR description LIKE '%{keyword}%'
        LIMIT 20;
        """
        
        print(f"\nSearching for: {keyword}")
        print("-" * 70)
        results = self.execute_query(sql)
        if results is not None:
            self.display_results(results)
    
    def run(self):
        """Main interface loop"""
        print("\n✓ Database ready for queries!\n")
        
        while True:
            self.show_menu()
            choice = input("Enter your choice (0-13): ").strip()
            
            if choice == '0':
                print("\n✓ Goodbye!\n")
                break
            elif choice == '12':
                self.search_by_keyword()
            elif choice == '13':
                self.run_custom_query()
            elif choice in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']:
                self.run_quick_query(choice)
            else:
                print("Invalid choice! Please try again.")
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("Connection closed.")

def main():
    script_dir = Path(__file__).parent
    db_path = script_dir / "netflix.db"
    
    if not db_path.exists():
        print(f"✗ Database not found: {db_path}")
        print("Please run: python setup_sqlite.py")
        sys.exit(1)
    
    interface = NetflixQueryInterface(str(db_path))
    try:
        interface.run()
    finally:
        interface.close()

if __name__ == "__main__":
    main()
