#!/usr/bin/env python3
"""
Netflix SQL Project - Query Runner
Executes all 15 business problem solutions
"""

import sqlite3
import os
from pathlib import Path

QUERIES = {
    1: {
        "title": "Count the number of Movies vs TV Shows",
        "sql": """
        SELECT 
            type,
            COUNT(*) as count
        FROM netflix
        GROUP BY type
        ORDER BY count DESC;
        """
    },
    2: {
        "title": "Find the most common rating for movies and TV shows",
        "sql": """
        WITH RatingCounts AS (
            SELECT 
                type,
                rating,
                COUNT(*) AS rating_count
            FROM netflix
            GROUP BY type, rating
        ),
        RankedRatings AS (
            SELECT 
                type,
                rating,
                rating_count,
                RANK() OVER (PARTITION BY type ORDER BY rating_count DESC) AS rank
            FROM RatingCounts
        )
        SELECT 
            type,
            rating AS most_frequent_rating,
            rating_count
        FROM RankedRatings
        WHERE rank = 1
        ORDER BY type;
        """
    },
    3: {
        "title": "List all movies released in a specific year (e.g., 2020)",
        "sql": """
        SELECT 
            show_id,
            title,
            type,
            release_year,
            rating,
            duration
        FROM netflix
        WHERE release_year = 2020 AND type = 'Movie'
        LIMIT 10;
        """
    },
    4: {
        "title": "Find the top 5 countries with the most content on Netflix",
        "sql": """
        SELECT 
            country,
            COUNT(*) as total_content
        FROM (
            SELECT 
                TRIM(country) as country
            FROM netflix,
            (SELECT '' UNION SELECT ',')
            WHERE country != ''
            AND country IS NOT NULL
        )
        WHERE country != ''
        GROUP BY country
        ORDER BY total_content DESC
        LIMIT 5;
        """
    },
    5: {
        "title": "Identify the longest movie",
        "sql": """
        SELECT 
            title,
            type,
            duration,
            release_year
        FROM netflix
        WHERE type = 'Movie'
        ORDER BY CAST(
            SUBSTR(duration, 1, INSTR(duration, ' ') - 1) AS INTEGER
        ) DESC
        LIMIT 1;
        """
    },
    6: {
        "title": "Find content added in the last 5 years",
        "sql": """
        SELECT 
            title,
            type,
            date_added,
            release_year
        FROM netflix
        WHERE date_added IS NOT NULL
        AND date_added != ''
        ORDER BY date_added DESC
        LIMIT 20;
        """
    },
    7: {
        "title": "Find all movies/TV shows by director 'Rajiv Chilaka'",
        "sql": """
        SELECT 
            title,
            type,
            director,
            release_year
        FROM netflix
        WHERE director LIKE '%Rajiv Chilaka%'
        LIMIT 20;
        """
    },
    8: {
        "title": "List all TV shows with more than 5 seasons",
        "sql": """
        SELECT 
            title,
            type,
            duration,
            release_year
        FROM netflix
        WHERE type = 'TV Show'
        AND CAST(SUBSTR(duration, 1, INSTR(duration, ' ') - 1) AS INTEGER) > 5
        ORDER BY CAST(SUBSTR(duration, 1, INSTR(duration, ' ') - 1) AS INTEGER) DESC
        LIMIT 20;
        """
    },
    9: {
        "title": "Count the number of content items in each genre",
        "sql": """
        SELECT 
            TRIM(genre) as genre,
            COUNT(*) as total_content
        FROM (
            SELECT 
                TRIM(substr(listed_in, 0, instr(listed_in || ',', ','))) as genre,
                listed_in
            FROM netflix
            WHERE listed_in IS NOT NULL
        )
        WHERE genre != ''
        GROUP BY genre
        ORDER BY total_content DESC
        LIMIT 20;
        """
    },
    10: {
        "title": "Find each year and the average numbers of content release in India. Return top 5 years with highest avg content release!",
        "sql": """
        SELECT 
            release_year,
            COUNT(*) as total_release,
            ROUND(100.0 * COUNT(*) / 
                (SELECT COUNT(*) FROM netflix WHERE country LIKE '%India%'), 2) AS avg_release_percent
        FROM netflix
        WHERE country LIKE '%India%'
        GROUP BY release_year
        ORDER BY avg_release_percent DESC
        LIMIT 5;
        """
    },
    11: {
        "title": "List all movies that are documentaries",
        "sql": """
        SELECT 
            title,
            type,
            listed_in,
            release_year
        FROM netflix
        WHERE listed_in LIKE '%Documentaries%'
        LIMIT 20;
        """
    },
    12: {
        "title": "Find all content without a director",
        "sql": """
        SELECT 
            title,
            type,
            release_year,
            rating
        FROM netflix
        WHERE director IS NULL OR director = ''
        LIMIT 20;
        """
    },
    13: {
        "title": "Find how many movies actor 'Salman Khan' appeared in last 10 years",
        "sql": """
        SELECT 
            title,
            type,
            casts,
            release_year
        FROM netflix
        WHERE casts LIKE '%Salman Khan%'
        AND release_year >= (
            SELECT MAX(CAST(release_year AS INTEGER)) - 10 FROM netflix
        )
        ORDER BY release_year DESC
        LIMIT 20;
        """
    },
    14: {
        "title": "Find the top 10 actors who have appeared in the highest number of movies produced in India",
        "sql": """
        SELECT 
            actor,
            COUNT(*) as appearances
        FROM (
            SELECT 
                TRIM(actor) as actor
            FROM netflix,
            (WITH RECURSIVE split(actor, remaining) AS (
                SELECT '', casts || ','
                FROM netflix
                WHERE country LIKE '%India%'
                UNION ALL
                SELECT 
                    TRIM(SUBSTR(remaining, 1, INSTR(remaining, ',') - 1)),
                    SUBSTR(remaining, INSTR(remaining, ',') + 1)
                FROM split
                WHERE remaining != ''
            )
            SELECT actor FROM split WHERE actor != '')
            WHERE country LIKE '%India%'
        )
        WHERE actor != ''
        GROUP BY actor
        ORDER BY appearances DESC
        LIMIT 10;
        """
    },
    15: {
        "title": "Categorize content based on 'kill' and 'violence' keywords. Label 'Bad' if keywords present, 'Good' otherwise",
        "sql": """
        SELECT 
            category,
            COUNT(*) AS content_count
        FROM (
            SELECT 
                CASE 
                    WHEN description LIKE '%kill%' 
                         OR description LIKE '%violence%'
                         OR description LIKE '%Kill%'
                         OR description LIKE '%Violence%'
                    THEN 'Bad'
                    ELSE 'Good'
                END AS category
            FROM netflix
        ) AS categorized_content
        GROUP BY category
        ORDER BY content_count DESC;
        """
    }
}

def connect_db(db_path):
    """Connect to SQLite database"""
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"✗ Error connecting to database: {e}")
        return None

def print_results(title, results):
    """Pretty print query results"""
    print(f"\n{'='*80}")
    print(f"Query: {title}")
    print('='*80)
    
    if not results:
        print("No results returned")
        return
    
    # Get column names
    columns = [desc[0] for desc in results[0].keys()]
    
    # Print headers
    col_widths = [max(len(col), 20) for col in columns]
    header = " | ".join(col.ljust(width) for col, width in zip(columns, col_widths))
    print(header)
    print("-" * len(header))
    
    # Print rows
    for row in results:
        values = [str(row[col])[:col_widths[i]-1] for i, col in enumerate(columns)]
        print(" | ".join(val.ljust(width) for val, width in zip(values, col_widths)))
    
    print(f"\nTotal rows: {len(results)}\n")

def run_all_queries(db_path):
    """Execute all 15 queries"""
    conn = connect_db(db_path)
    if not conn:
        return
    
    print("\n" + "="*80)
    print("NETFLIX SQL PROJECT - ALL QUERIES EXECUTION")
    print("="*80)
    
    cursor = conn.cursor()
    successful = 0
    failed = 0
    
    for query_num in sorted(QUERIES.keys()):
        try:
            query_info = QUERIES[query_num]
            cursor.execute(query_info["sql"])
            results = cursor.fetchall()
            
            print_results(f"#{query_num}: {query_info['title']}", results)
            successful += 1
        except Exception as e:
            print(f"\n✗ Query {query_num} Failed: {str(e)}\n")
            failed += 1
    
    conn.close()
    
    print("\n" + "="*80)
    print(f"SUMMARY: {successful} successful | {failed} failed out of {len(QUERIES)} queries")
    print("="*80 + "\n")

if __name__ == "__main__":
    script_dir = Path(__file__).parent
    db_path = script_dir / "netflix.db"
    
    if not db_path.exists():
        print(f"✗ Database not found: {db_path}")
        print("Please run: python setup_sqlite.py")
        exit(1)
    
    run_all_queries(str(db_path))
