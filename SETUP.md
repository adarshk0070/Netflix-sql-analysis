# Netflix SQL Project Setup Guide

This guide will help you set up and run the Netflix SQL analysis project locally.

## Prerequisites

You need **PostgreSQL 12+** installed on your system. This project uses PostgreSQL-specific features like:
- `UNNEST()` and `STRING_TO_ARRAY()` functions
- Window functions (`RANK() OVER PARTITION BY`)
- Date manipulation functions

---

## Installation Options

### **Option 1: Install PostgreSQL on Windows (Recommended)**

#### Step 1: Download PostgreSQL Installer
1. Visit: https://www.postgresql.org/download/windows/
2. Download the latest PostgreSQL installer (version 15 or newer)
3. Run the installer as **Administrator**

#### Step 2: Installation Settings
During installation, you'll be prompted for:
- **Installation Directory**: Keep default `C:\Program Files\PostgreSQL\15`
- **Password**: Set a secure password for the `postgres` user (remember this!)
- **Port**: Keep default `5432`
- **Locale**: Select your locale
- **Stack Builder**: Optional components (pgAdmin4 is recommended)

#### Step 3: Verify Installation
Open Command Prompt and run:
```cmd
psql --version
```

You should see: `psql (PostgreSQL) 15.x.x`

---

### **Option 2: Use PostgreSQL on Windows Subsystem for Linux (WSL)**

If you have WSL2 enabled:
```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
sudo service postgresql start
```

---

### **Option 3: Use Online PostgreSQL (No Installation)**

Use free online PostgreSQL services:
- **ElephantSQL** (elephantsql.com) - Free tier available
- **Railway.app** - Quick deployment
- **Render** - PostgreSQL as a service

---

## Setting Up the Netflix Database

### **Step 1: Create a Database**

Open Command Prompt and connect to PostgreSQL:
```cmd
psql -U postgres
```

When prompted, enter your PostgreSQL password set during installation.

Then run:
```sql
CREATE DATABASE netflix_db;
```

Exit psql:
```sql
\q
```

### **Step 2: Create the Table Schema**

Navigate to your project directory and run:
```cmd
psql -U postgres -d netflix_db -f Schemas.sql
```

Verify the table was created:
```cmd
psql -U postgres -d netflix_db -c "SELECT * FROM netflix LIMIT 5;"
```

### **Step 3: Import CSV Data**

Create a temporary import script. Save this as `import_data.sql`:

```sql
COPY netflix(show_id, type, title, director, casts, country, date_added, release_year, rating, duration, listed_in, description)
FROM 'C:\Users\Adarsh\Downloads\sql project\netflix_sql_project-main\netflix_titles.csv'
WITH (FORMAT csv, HEADER true, DELIMITER ',', QUOTE '"', ESCAPE '"', NULL '');
```

Then run:
```cmd
psql -U postgres -d netflix_db -f import_data.sql
```

### **Step 4: Verify Data Import**

Check the data was imported successfully:
```cmd
psql -U postgres -d netflix_db -c "SELECT COUNT(*) FROM netflix;"
```

You should see approximately **8,800+ records** imported.

---

## Running the Queries

### **Option A: Run All Solutions at Once**

```cmd
psql -U postgres -d netflix_db -f "Solutions of 15 business problems.sql"
```

### **Option B: Run Individual Queries in pgAdmin4**

1. Open **pgAdmin 4** (installed with PostgreSQL)
2. Login with your credentials
3. Navigate: **Servers → PostgreSQL → Databases → netflix_db**
4. Click the **Query Tool** icon
5. Copy-paste queries from `Solutions of 15 business problems.sql`
6. Execute them one by one

### **Option C: Connect from Command Line Interactively**

```cmd
psql -U postgres -d netflix_db
```

Then paste individual SQL queries from the solutions file.

---

## 15 Business Questions Solved

| # | Question |
|---|----------|
| 1 | Count the number of Movies vs TV Shows |
| 2 | Find the most common rating for movies and TV shows |
| 3 | List all movies released in a specific year (e.g., 2020) |
| 4 | Find the top 5 countries with the most content |
| 5 | Identify the longest movie |
| 6 | Find content added in the last 5 years |
| 7 | Find all movies/TV shows by director 'Rajiv Chilaka' |
| 8 | List all TV shows with more than 5 seasons |
| 9 | Count the number of content items in each genre |
| 10 | Find average content release by India by year (top 5) |
| 11 | List all movies that are documentaries |
| 12 | Find all content without a director |
| 13 | Find movies with actor 'Salman Khan' (last 10 years) |
| 14 | Find top 10 actors in Indian-produced movies |
| 15 | Categorize content based on 'kill' and 'violence' keywords |

---

## Troubleshooting

### **Error: "psql: command not found"**
- PostgreSQL is not installed or not in PATH
- Solution: Reinstall PostgreSQL and ensure it's added to PATH, or use full path: `C:\Program Files\PostgreSQL\15\bin\psql.exe`

### **Error: "role 'postgres' does not exist"**
- Run as Administrator and verify PostgreSQL service is running
- On Windows Services, ensure "postgresql-x64-15" service is started

### **Error: "could not connect to server"**
- PostgreSQL service is not running
- Start it: `Services → PostgreSQL → Start`
- Or from Command Prompt (as Admin): `pg_ctl -D "C:\Program Files\PostgreSQL\15\data" start`

### **CSV Import Fails**
- Ensure the CSV path is correct and uses **forward slashes** `/` or escaped backslashes `\\`
- Check that the CSV file exists
- Verify column names match exactly in the COPY command

### **COPY Command Issues**
An alternative method to import CSV:

1. Create a small Python script `import_csv.py`:
```python
import pandas as pd
import psycopg2

df = pd.read_csv('netflix_titles.csv')
conn = psycopg2.connect(
    host='localhost',
    database='netflix_db',
    user='postgres',
    password='YOUR_PASSWORD'
)
cursor = conn.cursor()

for idx, row in df.iterrows():
    cursor.execute("""
        INSERT INTO netflix VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, tuple(row))
    
conn.commit()
cursor.close()
conn.close()
print("Import complete!")
```

2. Run: `python import_csv.py`

---

## Using pgAdmin4 GUI (Recommended for Beginners)

1. Launch **pgAdmin4** (installed with PostgreSQL)
2. Login to your local server
3. Right-click **Databases** → **Create** → **Database**
4. Name it `netflix_db`
5. Right-click the database → **Restore**
6. Select `Schemas.sql` to create the table
7. Use Query Tool to import CSV and run queries

---

## Next Steps

Once setup is complete:
1. Run all 15 SQL solutions
2. Analyze the results
3. Modify queries for deeper insights
4. Create your own custom analyses

---

## Support

If you encounter issues:
1. Check PostgreSQL is running: `Services` → search "postgres"
2. Verify connection: `psql -U postgres -c "SELECT version();"`
3. Check file paths use forward slashes or escaped backslashes
4. Ensure CSV file is in the correct location

Good luck with your Netflix SQL analysis! 🎬📊
