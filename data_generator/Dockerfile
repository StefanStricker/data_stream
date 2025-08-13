FROM python:3.9-slim

WORKDIR /app
COPY data_generation.py .

RUN pip install flask numpy prometheus_client

CMD ["python", "data_generation.py"]