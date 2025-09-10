# query_api.py
from flask import Flask, jsonify, request
from pymongo import MongoClient
from datetime import datetime, timedelta

app = Flask(__name__)

client = MongoClient("mongodb://mongodb:27017/")
db = client["sensor_db"]
collection = db["measurements"]

@app.get("/sensors")
def get_sensors():

    limit = int(request.args.get("limit", 500))
    docs = collection.find(
        {},
        {"_id": 0, "timestamp": 1,
         "temperature_data": 1,
         "humidity_data": 1,
         "cloud_data": 1,
         "wind_data": 1,
         "percipation_data": 1}
    ).sort("timestamp", -1).limit(limit)

    data = []
    for d in docs:

        iso_time = d["timestamp"].isoformat()
        
        data.append({
            "time": iso_time,   
            "temperature": d["temperature_data"],
            "humidity": d["humidity_data"],
            "cloud": d["cloud_data"],
            "wind": d["wind_data"],
            "percipation": d["percipation_data"]
        })

    return jsonify(data[::-1]) 

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)