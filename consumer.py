from kafka import KafkaConsumer
import json

running = True

consumer = KafkaConsumer(
    "sensor-data",
    bootstrap_servers= "localhost:9092",
    auto_offset_reset = "earliest",
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    enable_auto_commit=False,
    group_id="mongo-writer-group",
)

while running:
    try:
        for message in consumer:
            data = message.value
            print(f"Recieved: {data}")
            consumer.commit_async()

    except Exception as e:
        print(f"Error: {str(e)}")            

