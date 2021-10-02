import sqlite3
import datetime

conn = sqlite3.connect('database.db')
print("Opened database successfully")

# NOTE: ID is DEPRECATED
conn.execute('CREATE TABLE simulated (id TEXT, lat NUMERIC, lon NUMERIC, alt NUMERIC, time TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')
conn.execute('CREATE TABLE locations (id TEXT, lat NUMERIC, lon NUMERIC, alt NUMERIC, time TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')
print("Table created successfully")
conn.close()