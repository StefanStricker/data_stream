import numpy as np
from datetime import datetime
from flask import Flask, jsonify
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

#parameters
temperature_mean = 20
temperature_std = 5
humidity_mean = 50
humidity_std = 15
cloud_mean = 36
cloud_std = 7
wind_mean = 11
wind_std= 2
percipation_mean = 5
percipation_std = 2

#Prometheus metrics
GEN_TOTAL      = Counter("generator_events_total", "Total generated sensor events")
GEN_ERRORS     = Counter("generator_errors_total", "Total errors during generation")
GEN_LATENCY    = Histogram("generator_latency_seconds", "Generation function latency (seconds)")

def data_properties():
    with GEN_LATENCY.time():
        return{
            "timestamp": datetime.now().isoformat(),
            "temperature_data": np.random.normal(temperature_mean, temperature_std),
            "humidity_data": np.random.normal(humidity_mean, humidity_std),
            "cloud_data": np.random.normal(cloud_mean, cloud_std),
            "wind_data": np.random.normal(wind_mean, wind_std),
            "percipation_data": np.random.normal(percipation_mean, percipation_std)
        }

@app.route("/data_generator", methods=["GET"])
def get_data():
    try:
        data = data_properties()
        GEN_TOTAL.inc()
        return jsonify(data)
    except Exception:
        GEN_ERRORS.inc()
        raise    

@app.get("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ =="__main__":
    app.run(host="0.0.0.0", port=5000)


