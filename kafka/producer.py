import pandas as pd
from kafka import KafkaProducer
import time
import json
import requests

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"))

while True:
    try:
        response = requests.get("http://localhost:5000/data_generator")
        if response.ok:
            data = response.json()
            producer.send("sensor-data", value = data)
            print(f"Sent: {data}")
        else:
            print("API error:", response.status_code)
    except Exception as e:
        print("Error:", e)

    time.sleep(1)                

producer.flush()    