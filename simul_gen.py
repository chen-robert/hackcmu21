from simul_data_paths import data_gen
import sqlite3
import glob
import json
import uuid
import time

paths = []
for path in glob.iglob("data/*"):
    with open(path) as f:
        print(path)
        paths.append(json.load(f))

start = time.time()

data = data_gen(paths)

end = time.time()

print("generated", len(data), "series in", end - start, "s")

db_data = []
for pts in data:
  user_id = str(uuid.uuid4())
  
  for pt in pts:
    db_data.append({
      "id": user_id,
      "lat": pt["lat"],
      "lon": pt["lon"],
      "alt": 0,
      "time": pt["time"]
    })
  
print("processed data to", len(db_data), "points")

conn = sqlite3.connect('database.db')
print("Opened database successfully")

print("deleting")
conn.execute("DELETE FROM simulated")
conn.commit()
print("inserting")
conn.executemany('INSERT INTO simulated (id, lat, lon, alt, time) VALUES (:id, :lat, :lon, :alt, :time)', db_data)
conn.commit()

conn.close()

print("done")