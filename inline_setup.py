import sqlite3,csv,os
os.chdir(os.path.dirname(__file__))
db=sqlite3.connect('netflix.db')
c=db.cursor()
c.execute('DROP TABLE IF EXISTS netflix')
c.execute('''CREATE TABLE netflix(show_id TEXT,type TEXT,title TEXT,director TEXT,casts TEXT,country TEXT,date_added TEXT,release_year INTEGER,rating TEXT,duration TEXT,listed_in TEXT,description TEXT)''')
with open('netflix_titles.csv',encoding='utf-8')as f:
    r=list(csv.reader(f))[1:]
    c.executemany('INSERT INTO netflix VALUES(?,?,?,?,?,?,?,?,?,?,?,?)',r)
db.commit()
c.execute('SELECT COUNT(*) FROM netflix')
print(c.fetchone()[0],'records imported')
db.close()
print('Setup complete! Database ready.')
