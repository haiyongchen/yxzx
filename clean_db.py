import sqlite3
import os

db = 'C:/Users/63111/.hermes/state.db'
conn = sqlite3.connect(db)
c = conn.cursor()

# List tables
c.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = c.fetchall()
print('Tables:', [t[0] for t in tables])

# Clean all tables
for (tname,) in tables:
    try:
        c.execute(f'DELETE FROM {tname}')
        if c.rowcount > 0:
            print(f'Cleaned {tname} ({c.rowcount} rows)')
    except:
        pass

conn.commit()
conn.close()
print('Database cleaned!')
