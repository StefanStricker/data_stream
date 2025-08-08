import numpy as np
from datetime import datetime
import json
import time
from flask import Flask, jsonify

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

def data_properties():
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
    data = data_properties()
    return jsonify(data)


if __name__ =="__main__":
    app.run(host="0.0.0.0", port=5000)


