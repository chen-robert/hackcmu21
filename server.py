from flask import Flask, request, jsonify, g
from datetime import datetime, timedelta, timezone
from collections import Counter
import os, sqlite3

app = Flask(__name__, static_url_path="", static_folder="static/dist")

# timeStart
# timeEnd
# returns => [{ x, y, magnitude }]
@app.get("/api/v1/locations")
def locations():
    now = datetime.now(timezone.utc)
    return locations_query(now - timedelta(minutes=30), now)

@app.get("/api/v1/locations/<int:start>/<int:end>")
def locations_interval(start, end):
    return locations_query(datetime.fromtimestamp(start, timezone.utc), datetime.fromtimestamp(end, timezone.utc))

@app.get("/api/v1/simulated/locations/<int:start>/<int:end>")
def simulated_locations_interval(start, end):
    return locations_query(datetime.fromtimestamp(start, timezone.utc), datetime.fromtimestamp(end, timezone.utc), simulated=True)

@app.get("/api/v1/simulated/locations")
def simulated_locations():
    now = datetime.now(timezone.utc)
    return locations_query(now - timedelta(minutes=30), now, simulated=True)

@app.get("/api/v1/data")
def data():
    now = datetime.now(timezone.utc)
    return locations_data(now - timedelta(minutes=30), now)

@app.get("/api/v1/data/<int:start>/<int:end>")
def data_interval(start, end):
    return locations_data(datetime.fromtimestamp(start, timezone.utc), datetime.fromtimestamp(end, timezone.utc))

@app.get("/api/v1/simulated/data/<int:start>/<int:end>")
def simulated_data_interval(start, end):
    return locations_data(datetime.fromtimestamp(start, timezone.utc), datetime.fromtimestamp(end, timezone.utc), simulated=True)


def normalize_point(lat, lon):
    return round(lat, 6), round(lon, 6)

def locations_query(start, end, simulated=False):
    cur = get_db().cursor()
    table = "simulated" if simulated else "locations"
    cur.execute(f"SELECT id, lat, lon, time FROM {table} WHERE ? <= time AND time <= ?", (start, end))

    data = {}
    for id, lat, lon, time in cur:
        if id not in data or time > data[id][2]:
            data[id] = lat, lon, time

    return create_response(normalize_point(lat, lon) for lat, lon, time in data.values())

def locations_data(start, end, simulated=False):
    cur = get_db().cursor()
    table = "simulated" if simulated else "locations"
    cur.execute(f"SELECT lat, lon FROM {table} WHERE ? <= time AND time <= ?", (start, end))
    return create_response(normalize_point(lat, lon) for lat, lon in cur)

def create_response(data):
    bins = Counter(data)
    resp = jsonify([{"lat": lat, "lon": lon, "value": val} for (lat, lon), val in bins.items()])
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp

# @app.get("/api/v1/debug")
# def debug():
#     cur = get_db().cursor()
#     cur.execute("SELECT * FROM locations")
#     return jsonify(cur.fetchall())
# 
# # POST
# # id
# # location: {x, y, z}
# @app.post("/api/v1/upload")
# def upload():
#     conn = get_db()
#     # cur_time = datetime.datetime.now()
#     conn.execute("INSERT INTO locations (id, lat, lon, alt) VALUES (:id, :lat, :lon, :alt)", request.json)
#     conn.commit()
#     return jsonify(request.json)
# 
# # POST
# # id
# # location: {x, y, z}
# @app.post("/api/v1/simulated/upload")
# def simulated_upload():
#     conn = get_db()
#     # cur_time = datetime.datetime.now()
#     conn.execute("INSERT INTO simulated (id, lat, lon, alt) VALUES (:id, :lat, :lon, :alt)", request.json)
#     conn.commit()
#     return jsonify(request.json)
# 
# @app.get("/api/v1/simulated/debug")
# def simulated_debug():
#     cur = get_db().cursor()
#     cur.execute("SELECT * FROM simulated")
#     return jsonify(cur.fetchall())
# 
# @app.post("/api/v1/simulated/dropall")
# def simulated_dropall():
#     conn = get_db()
#     # cur_time = datetime.datetime.now()
#     conn.execute("DELETE FROM simulated", request.json)
#     conn.commit()
#     return "dropped"

# DB CODE

DATABASE = os.environ.get("DATABASE_PATH", "./database.db")

def get_db():
    db = getattr(g, "_database", None)

    if db is None:
        db = g._database = sqlite3.connect(DATABASE, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()