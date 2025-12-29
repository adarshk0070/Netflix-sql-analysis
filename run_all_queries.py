#!/usr/bin/env python3
import sqlite3
from pathlib import Path

db_path = Path(__file__).parent / "netflix.db"

QUERIES = [
    ("Count the number of Movies vs TV Shows", 
     "SELECT type, COUNT(*) as count FROM netflix GROUP BY type ORDER BY count DESC"),
    
    ("Find the most common rating for movies and TV shows",
     """SELECT type, rating, COUNT(*) as count 
        FROM netflix 
        GROUP BY type, rating 
        ORDER BY type, count DESC"""),
    
    ("List all movies released in a specific year (e.g., 2020)",
     "SELECT title, type, release_year, rating FROM netflix WHERE release_year = 2020 AND type = 'Movie' LIMIT 15"),
    
    ("Find the top 5 countries with the most content",
     """SELECT country, COUNT(*) as total_content 
        FROM netflix 
        WHERE country IS NOT NULL AND country != ''
        GROUP BY country 
        ORDER BY total_content DESC 
        LIMIT 5"""),
    
    ("Identify the longest movie",
     """SELECT title, duration FROM netflix 
        WHERE type = 'Movie' AND duration IS NOT NULL
        ORDER BY CAST(SUBSTR(duration, 1, INSTR(duration, ' ') - 1) AS INTEGER) DESC 
        LIMIT 1"""),
    
    ("Find content added in the last 5 years",
     """SELECT title, type, date_added FROM netflix 
        WHERE date_added IS NOT NULL AND date_added != ''
        ORDER BY date_added DESC 
        LIMIT 10"""),
    
    ("Find all movies/TV shows by director 'Rajiv Chilaka'",
     """SELECT title, type, director FROM netflix 
        WHERE director LIKE '%Rajiv Chilaka%' 
        LIMIT 10"""),
    
    ("List all TV shows with more than 5 seasons",
     """SELECT title, duration FROM netflix 
        WHERE type = 'TV Show' 
        AND CAST(SUBSTR(duration, 1, INSTR(duration, ' ') - 1) AS INTEGER) > 5
        ORDER BY CAST(SUBSTR(duration, 1, INSTR(duration, ' ') - 1) AS INTEGER) DESC 
        LIMIT 10"""),
    
    ("Count the number of content items in each genre",
     """SELECT listed_in as genre, COUNT(*) as total_content 
        FROM netflix 
        WHERE listed_in IS NOT NULL
        GROUP BY listed_in 
        ORDER BY total_content DESC 
        LIMIT 20"""),
    
    ("Average content release from India by year (top 5)",
     """SELECT release_year, COUNT(*) as total_release
        FROM netflix 
        WHERE country LIKE '%India%'
        GROUP BY release_year 
        ORDER BY total_release DESC 
        LIMIT 5"""),
    
    ("List all movies that are documentaries",
     """SELECT title, type, rating FROM netflix 
        WHERE listed_in LIKE '%Documentaries%' 
        LIMIT 10"""),
    
    ("Find all content without a director",
     """SELECT title, type, release_year FROM netflix 
        WHERE director IS NULL OR director = '' 
        LIMIT 10"""),
    
    ("Find movies with actor 'Salman Khan' (last 10 years)",
     """SELECT title, casts, release_year FROM netflix 
        WHERE casts LIKE '%Salman Khan%' 
        ORDER BY release_year DESC 
        LIMIT 10"""),
    
    ("Find the top 10 actors in Indian-produced movies",
     """SELECT casts, COUNT(*) as appearances 
        FROM netflix 
        WHERE country LIKE '%India%'
        GROUP BY casts 
        ORDER BY appearances DESC 
        LIMIT 10"""),
    
    ("Categorize content by 'kill' and 'violence' keywords",
     """SELECT 
        CASE WHEN description LIKE '%kill%' OR description LIKE '%Kill%' 
             OR description LIKE '%violence%' OR description LIKE '%Violence%'
        THEN 'Bad' ELSE 'Good' END as category,
        COUNT(*) as content_count 
        FROM netflix 
        GROUP BY category 
        ORDER BY content_count DESC"""),
]

def print_results(results, max_rows=20):
    """Pretty print query results"""
    if not results:
        print("  No results returned\n")
        return
    
    if not results[0]:
        print("  No results returned\n")
        return
    
    col_count = len(results[0])
    col_widths = [20] * col_count
    
    for row in results:
        for i, val in enumerate(row):
            col_widths[i] = max(col_widths[i], min(len(str(val)), 40))
    
    separator = " | ".join("-" * w for w in col_widths)
    
    print("  " + separator)
    for idx, row in enumerate(results):
        if idx >= max_rows:
            print(f"  ... and {len(results) - max_rows} more rows")
            break
        
        values = [str(v if v is not None else 'NULL')[:col_widths[i]] 
                  for i, v in enumerate(row)]
        line = " | ".join(val.ljust(width) for val, width in zip(values, col_widths))
        print("  " + line)
    
    print("  " + separator)
    print(f"  Total rows: {len(results)}\n")

def main():
    if not db_path.exists():
        print(f"Error: Database not found at {db_path}")
        return
    
    print("\n" + "="*80)
    print("NETFLIX SQL PROJECT - EXECUTING ALL 15 BUSINESS QUERIES")
    print("="*80 + "\n")
    
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    successful = 0
    failed = 0
    
    for idx, (title, sql) in enumerate(QUERIES, 1):
        print(f"Query {idx}: {title}")
        print("-" * 80)
        
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            print_results(results)
            successful += 1
        except Exception as e:
            print(f"  Error: {str(e)}\n")
            failed += 1
    
    conn.close()
    
    print("="*80)
    print(f"SUMMARY: {successful} successful | {failed} failed out of {len(QUERIES)} queries")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
