from kafka import KafkaProducer
import time
import json
import requests
import os

KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
GENERATOR_URL = os.getenv("GENERATOR_URL", "http://generator:5000/data_generator")
TOPIC = os.getenv("KAFKA_TOPIC", "sensor-data")


producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"))


while True:
    try:
        response = requests.get(GENERATOR_URL, timeout=3)
        if response.ok:
            data = response.json()
            producer.send(TOPIC, value = data)
            print(f"Sent: {data}")
        else:
            print("API error:", response.status_code)
    except Exception as e:
        print("Error:", e)

    time.sleep(1)                

producer.flush()    