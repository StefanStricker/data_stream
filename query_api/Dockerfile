FROM python:3.9-slim

WORKDIR /app
COPY query_api.py .
RUN pip install flask pymongo

CMD ["python", "query_api.py"]
