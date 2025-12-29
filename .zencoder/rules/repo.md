---
description: Repository Information Overview
alwaysApply: true
---

# Netflix Movies and TV Shows SQL Analysis - Repository Information

## Summary
This repository contains a comprehensive SQL-based data analysis project focused on Netflix's movies and TV shows dataset sourced from Kaggle. The project demonstrates advanced SQL techniques to extract insights and answer 15 distinct business problems related to content distribution, ratings, geography, actors, and content categorization.

## Structure
- **Schemas.sql**: Database schema definition for the netflix table with 12 columns (show_id, type, title, director, casts, country, date_added, release_year, rating, duration, listed_in, description)
- **Business Problems Netflix.sql**: List of 15 business questions to be answered through SQL analysis
- **Solutions of 15 business problems.sql**: Complete SQL implementations and solutions for all business problems
- **netflix_titles.csv**: Raw dataset containing Netflix titles data (3.24 MB)
- **README.md**: Comprehensive project documentation with objectives, solutions, and findings
- **logo.png**: Project branding asset

## Specification & Tools
**Type**: SQL Data Analysis Project  
**Database System**: PostgreSQL (based on SQL syntax: UNNEST, STRING_TO_ARRAY, SPLIT_PART, window functions, EXTRACT)  
**Data Format**: CSV (netflix_titles.csv)  
**Required Tools**: PostgreSQL database system, SQL client or IDE

## Key Resources

**Main Files**:
- `Schemas.sql` - Table creation and structure definition
- `Solutions of 15 business problems.sql` - 15 complete SQL solutions
- `netflix_titles.csv` - Raw data source for analysis

**Data Schema**:
The netflix table contains 12 columns: show_id (VARCHAR 5), type (VARCHAR 10), title (VARCHAR 250), director (VARCHAR 550), casts (VARCHAR 1050), country (VARCHAR 550), date_added (VARCHAR 55), release_year (INT), rating (VARCHAR 15), duration (VARCHAR 15), listed_in (VARCHAR 250), description (VARCHAR 550)

## Usage & Operations

**Setup Steps**:
1. Import the CSV data into PostgreSQL using the schema defined in `Schemas.sql`
2. Execute table creation script: `psql -U username -d database_name -f Schemas.sql`
3. Load data from `netflix_titles.csv` into the netflix table

**Key Business Questions Addressed**:
1. Content type distribution (Movies vs TV Shows)
2. Most common ratings by content type
3. Movies released in specific years
4. Top 5 countries with most Netflix content
5. Longest movie identification
6. Recently added content (last 5 years)
7. Content by specific director (e.g., Rajiv Chilaka)
8. TV shows with 5+ seasons
9. Content count by genre
10. Average content releases from India by year
11. Documentary content identification
12. Content without director information
13. Actor appearance count (e.g., Salman Khan, last 10 years)
14. Top 10 actors in Indian-produced movies
15. Content categorization based on violence/kill keywords

**SQL Techniques Demonstrated**:
- Window functions (RANK() OVER PARTITION BY)
- String manipulation (UNNEST, STRING_TO_ARRAY, SPLIT_PART)
- Date operations (TO_DATE, CURRENT_DATE, INTERVAL)
- Case statements and conditional logic
- Aggregate functions (COUNT, GROUP BY)
- Pattern matching (LIKE, ILIKE)
- Common Table Expressions (CTEs)

## Validation

**Data Quality Checks**:
- NULL handling for director and other optional fields
- String parsing and array operations for multi-value columns (country, casts, listed_in)
- Type casting for numeric comparisons (duration parsing as INT)
- Date format validation and conversion

**Analysis Verification**:
- All 15 business problems have tested SQL solutions
- Results validate content distribution, temporal trends, and categorical relationships
- Findings documented in README with business insights and conclusions
