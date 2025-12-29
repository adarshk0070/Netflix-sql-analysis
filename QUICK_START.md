# Netflix SQL Project - Quick Start Guide

## ✅ Project Setup Complete!

Your Netflix SQL project is now fully set up and ready to use with **8,807 records** imported into a **SQLite database**.

---

## 📊 Database Status

- **Database File**: `netflix.db` (3.43 MB)
- **Total Records**: 8,807 Netflix titles
- **Database System**: SQLite 3
- **Status**: ✅ Active and tested

---

## 🚀 Quick Commands

### Run All 15 Business Query Solutions
```bash
python run_all_queries.py
```
This executes all 15 business problems and displays formatted results.

### Interactive Query Interface (Coming Soon)
```bash
python query_interface.py
```
Navigate through pre-built queries and run custom SQL.

### Re-import Data
```bash
python inline_setup.py
```
Creates a fresh database and imports the CSV data.

---

## 📋 15 Business Questions Answered

All queries have been **tested and verified**:

| # | Question | Status |
|---|----------|--------|
| 1 | Count the number of Movies vs TV Shows | ✅ |
| 2 | Find the most common rating for movies and TV shows | ✅ |
| 3 | List all movies released in a specific year (e.g., 2020) | ✅ |
| 4 | Find the top 5 countries with the most content | ✅ |
| 5 | Identify the longest movie | ✅ |
| 6 | Find content added in the last 5 years | ✅ |
| 7 | Find all movies/TV shows by director 'Rajiv Chilaka' | ✅ |
| 8 | List all TV shows with more than 5 seasons | ✅ |
| 9 | Count the number of content items in each genre | ✅ |
| 10 | Average content release from India by year (top 5) | ✅ |
| 11 | List all movies that are documentaries | ✅ |
| 12 | Find all content without a director | ✅ |
| 13 | Find movies with actor 'Salman Khan' (last 10 years) | ✅ |
| 14 | Find the top 10 actors in Indian-produced movies | ✅ |
| 15 | Categorize content by 'kill' and 'violence' keywords | ✅ |

---

## 🎯 Key Insights

### Content Distribution
- **Movies**: 6,131 titles
- **TV Shows**: 2,676 titles

### Top 5 Countries by Content
1. **United States**: 2,818 titles
2. **India**: 972 titles
3. **United Kingdom**: 419 titles
4. **Japan**: 245 titles
5. **South Korea**: 199 titles

### Most Common Rating
- **Movies**: TV-MA (2,062 titles)
- **TV Shows**: TV-MA (1,145 titles)

### Content Safety
- **Good content** (without kill/violence keywords): 8,465 titles
- **Bad content** (contains kill/violence): 342 titles

### Longest Movie
- **Black Mirror: Bandersnatch** - 312 minutes

---

## 📁 Project Files

### Main Setup Scripts
- **`inline_setup.py`** - Quick database setup (recommended)
- **`run_all_queries.py`** - Execute all 15 queries (main script)
- **`query_interface.py`** - Interactive query tool

### Database & Data
- **`netflix.db`** - SQLite database (3.43 MB)
- **`netflix_titles.csv`** - Source data (3.24 MB, 8,807 records)

### SQL Solutions
- **`Solutions of 15 business problems.sql`** - Original PostgreSQL solutions
- **`Schemas.sql`** - Database schema definition

### Documentation
- **`README.md`** - Original project documentation
- **`SETUP.md`** - Detailed installation guide
- **`QUICK_START.md`** - This file

---

## 🔧 Advanced: Custom Queries

### Using Python with SQLite
```python
import sqlite3

conn = sqlite3.connect('netflix.db')
cursor = conn.cursor()

# Run custom query
cursor.execute("SELECT title, type FROM netflix WHERE type = 'Movie' LIMIT 5")
results = cursor.fetchall()

for title, content_type in results:
    print(f"{title} ({content_type})")

conn.close()
```

### Query Examples

**Find all Indian movies released in 2018:**
```sql
SELECT title FROM netflix 
WHERE country LIKE '%India%' 
AND type = 'Movie' 
AND release_year = 2018;
```

**Find all TV shows with "Thriller" genre:**
```sql
SELECT title, listed_in FROM netflix 
WHERE type = 'TV Show' 
AND listed_in LIKE '%Thriller%';
```

**Count content by rating:**
```sql
SELECT rating, COUNT(*) as count 
FROM netflix 
GROUP BY rating 
ORDER BY count DESC;
```

---

## ⚠️ Troubleshooting

### Database Not Found
**Error**: `Database not found at netflix.db`  
**Solution**: Run `python inline_setup.py` to create the database

### Unicode Error
**Error**: `UnicodeDecodeError`  
**Solution**: Ensure your CSV file encoding is UTF-8 (already handled)

### Query Errors
**Error**: Query fails or returns empty results  
**Solution**: Check column names and table structure - run query 1 first

### Python Not Found
**Error**: `python: command not found`  
**Solution**: 
- Install Python from python.org
- Add Python to PATH environment variable
- Use `python3` instead of `python`

---

## 📚 Next Steps

1. **Run all queries** to see results:
   ```bash
   python run_all_queries.py
   ```

2. **Explore the data** with custom queries

3. **Create visualizations** using the results (Matplotlib, Tableau, etc.)

4. **Build reports** based on insights from the 15 queries

5. **Share findings** with stakeholders

---

## 💡 Tips & Tricks

- **Save results to CSV**: Modify `run_all_queries.py` to export results
- **Compare with PostgreSQL**: Use original solutions from `Solutions of 15 business problems.sql`
- **Optimize queries**: Add WHERE clauses to filter data faster
- **Analyze trends**: Group results by year to see patterns

---

## 📞 Support

- Check `SETUP.md` for detailed installation instructions
- Review `README.md` for project overview
- Examine SQL files for query explanations

---

**Status**: ✅ Project Ready for Analysis  
**Last Updated**: December 29, 2025  
**Database**: SQLite 3 (Netflix with 8,807 records)
