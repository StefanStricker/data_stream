# Data stream processing pipeline

### Prerequisites:
Docker https://docs.docker.com/get-started/get-docker/ <br />
Docker Compose https://docs.docker.com/compose/install/

### Installation Guide:

1. Clone Repository <br />
git clone https://github.com/StefanStricker/data_stream.git

    cd data_stream 

2. Start Environment <br />
docker compose up -d --build

3. Veryfy running containers <br />
docker ps

4. Tear down environment  <br />
docker compose down -v

### Access Grafana 

Grafana is available at: http://localhost:3000 <br />
Login is possible with username: admin; password: admin <br />
Preconfigured Dashboard is available under Dashboards -> Sensor_data <br />

Prometheus is available under http://localhost:9090

