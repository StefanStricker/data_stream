import pandas as pd
from kafka import KafkaProducer
import time
import json

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"))

df = pd.read_json("synthetic_data.json")

print(df.head())

