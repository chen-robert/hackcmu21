import flask
from flask import Flask, request, jsonify, g
import sqlite3
from datetime import datetime, timedelta, timezone
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
    now = datetime.now(timezone.utc)
    return locations_query(now - timedelta(minutes=300), now)

@app.get("/api/v1/locations/<int:start>/<int:end>")
def locations_interval(start, end):
    return locations_query(datetime.fromtimestamp(start), datetime.fromtimestamp(end))

@app.get("/api/v1/data")
def data():
    now = datetime.now(timezone.utc)
    return locations_data(now - timedelta(minutes=300), now)

@app.get("/api/v1/data/<int:start>/<int:end>")
def data_interval(start, end):
    return locations_data(datetime.fromtimestamp(start), datetime.fromtimestamp(end))

ROUNDING = 5
def normalize_point(lat, lon):
    return round(lat, ROUNDING), round(lon, ROUNDING)

def locations_query(start, end):
    cur = get_db().cursor()
    cur.execute("SELECT id, lat, lon, alt, time FROM locations WHERE ? <= time AND time <= ?", (start, end))

    data = {}
    for id, lat, lon, alt, time in cur:
        time = time.replace(tzinfo=timezone.utc).astimezone()
        if id not in data or time > data[id]["time"]:
            data[id] = {
                "id": id,
                "coords": normalize_point(lat, lon),
                "time": time
            }
    
    return create_response(data)

def locations_data(start, end):
    cur = get_db().cursor()
    cur.execute("SELECT id, lat, lon, alt, time FROM locations WHERE ? <= time AND time <= ?", (start, end))

    data = {}
    for n, (id, lat, lon, alt, time) in enumerate(cur):
        time = time.replace(tzinfo=timezone.utc).astimezone()
        data[n] = {"coords": normalize_point(lat, lon)}
    
    return create_response(data)

def create_response(data):
    bins = {}
    for person in data.values():
        bins[person["coords"]] = 1 + bins.get(person["coords"], 0)

    ret = []

    mn = min(bins.values()) if bins else 0
    mx = max(bins.values()) if bins else 0

    for (lat, lon), val in bins.items():
        ret.append({
            "lat": lat,
            "lon": lon,
            "val": val,
        })

    resp = jsonify({
        "data": ret,
        "max": mx,
        "min": mn
    })
    resp.headers['Access-Control-Allow-Origin'] = '*'

    return resp
    
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