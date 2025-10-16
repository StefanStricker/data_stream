# Data stream processing pipeline

This project simulates a real-world data streaming scenario of wheather-data for a smart-city application. <br />
A continuous flow of synthetic sensor readings is generated, published to Kafka, processed and vizualized in real time.


## Docker Architecture Overview:

1. **Data_generator** generates syntehtic wheather sensor data (temperature, humidity, cloud, wind, percipation) and exposes it through a Flask api. <br />
2. **Kafka Producer** reads generated data and publishes to a Kafka topic <br />
3. **Kafka Cluster (3 brokers)** replicates data across 3 Brokers in KRaft Mode (Replication Factor 3, in-sync Replicas 2) <br />
4. **Kafka Consumer** subscribes to the topic and writes data to MongoDB <br />
5. **Query_api** is the REST API for Grafana to query MongoDB via the Infinity Plugin <br />
6. **Prometheus** collects metrics from data_generator, Kafka, and MongoDB <br />
7. **Grafana** visualizes sensor data via the Infinity plugin and System Health metrics via Prometheus <br />





### Prerequisites:
Docker https://docs.docker.com/get-started/get-docker/ <br />
Docker Compose https://docs.docker.com/compose/install/

### Installation Guide:

1. Clone Repository <br />
```git clone https://github.com/StefanStricker/data_stream.git```

    ```cd data_stream```

2. Setup Proconfigured environment <br />
```cp .env.example .env```

3. Start Environment <br />
```docker compose up -d --build```

4. Veryfy running containers <br />
```docker ps```

5. Tear down environment  <br />
```docker compose down -v (shutdown Docker and remove Volumes)```<br />
```rm -f .env (Removes Preconfigured environment)```

### Access Grafana 

Grafana is available at: http://localhost:3000 <br />
Login is possible with username: admin; password: admin <br />
Preconfigured Dashboard is available under Dashboards -> Sensor_data <br />

### Failure recovery Test:

A Failure recovery test is included to evaluate the systems resilience in case of interruptions to a Kafka broker, Kafka Consumer, or MongoDB 

Run the Failure recovery Test <br />
```bash resilience_test.sh```


### Project Structure:

 
```data-stream/
├── data_generation/        
│   └── data_generation.py
├── kafka/
│   ├── producer/producer.py
│   └── consumer/consumer.py
├── query_api/query_api.py 
├── grafana/
│   ├── dashboards/sensor_dashboard.json
│   └── provisioning/
│       ├── datasources/datasources.yml
│       └── dashboards/dashboards.yml
├── prometheus.yml
├── docker-compose.yml
├── .env.example
├── resilience_test.sh     
└── README.md```