from flask import Flask, request, jsonify, g
import sqlite3
from datetime import datetime, timedelta
import os

app = Flask(__name__)

@app.get("/")
def hello_world():
    return "<p>Hi Robby!</p>"

# timeStart
# timeEnd
# returns => [{ x, y, magnitude }]
@app.get("/api/v1/locations")
def locations():
    return locations_query(datetime.now() - timedelta(minutes=30), datetime.now())

@app.get("/api/v1/locations/<int:start>/<int:end>")
def locations_interval(start, end):
    return locations_query(datetime.fromtimestamp(start), datetime.fromtimestamp(end))

ROUNDING = 3
def normalize_point(lat, lon):
    return round(lat, ROUNDING), round(lon, ROUNDING)

def locations_query(start, end):
    cur = get_db().cursor()
    cur.execute("SELECT id, lat, lon, alt, time FROM locations WHERE ? <= time AND time <= ?", (start, end))

    data = {}
    for id, lat, lon, alt, time in cur:
        print(repr(time), str(time), time.tzinfo)
        if id not in data or time > data[id]["time"]:
            data[id] = {
                "id": id,
                "coords": normalize_point(lat, lon),
                "alt": alt,
                "time": time
            }

    ret = {}
    for person in data.values():
        #ret.setdefault(person["coords"], []).append(person["id"])
        ret[person["coords"]] = 1 + ret.get(person["coords"], 0)

    return jsonify(ret)
    
@app.get("/api/v1/debug")
def debug():
    cur = get_db().cursor()
    cur.execute("SELECT * FROM locations")
    return jsonify(cur.fetchall())

# POST
# id
# location: {x, y, z} 
@app.post("/api/v1/upload")
def upload():
    print(request.json)
    conn = get_db()
    # cur_time = datetime.datetime.now()
    conn.execute("INSERT INTO locations (id, lat, lon, alt) VALUES (:id, :lat, :lon, :alt)", request.json)
    conn.commit()
    return jsonify(request.json)

# DB CODE

DATABASE = os.environ.get("DATABASE_PATH", './database.db')

def get_db():
    db = getattr(g, '_database', None)

    if db is None:
        db = g._database = sqlite3.connect(DATABASE, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()