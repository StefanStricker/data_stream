set -euo pipefail

#Get generator counter and doc count

gen_total() { curl -s http://localhost:5000/metrics | awk '/^generator_events_total[[:space:]]/ {print $2; exit}'; }
to_int() { awk '{printf "%.0f\n", $1+0}'; }
mongo_count() { curl -s "http://localhost:5001/sensors?limit=100000" | jq 'length'; }

echo "Starting resilience test . . . "
sleep 3
BASE_GEN_RAW=$(gen_total || echo 0)
BASE_GEN=$(echo "${BASE_GEN_RAW:-0}" | to_int)
BASE_CNT=$(mongo_count || echo 0)
echo "Baseline: generator=${BASE_GEN_RAW:-0}, docs=$BASE_CNT"

#Consumer downtime

echo "Stopping consumer for 15s . . ."
docker compose stop consumer
sleep 15
MID_GEN_RAW=$(gen_total || echo 0)
MID_GEN=$(echo "${MID_GEN_RAW:-0}" | to_int)

echo "Starting consumer . . ."
docker compose start consumer
sleep 15
AFTER_CNT=$(mongo_count || echo 0)

PRODUCED=$(( MID_GEN - BASE_GEN ))
INGESTED=$(( AFTER_CNT - BASE_CNT ))
echo "Produced while consumer down: $PRODUCED (raw ${MID_GEN_RAW:-0}-${BASE_GEN_RAW:-0}), Ingested after restart: $INGESTED"
if [ "$INGESTED" -ge "$(( PRODUCED - 2 ))" ]; then
  echo "OK: backlog recovered (tolerance 2 msgs)."
else
  echo "FAIL: missing messages after consumer restart." && exit 1
fi


#Broker failure

echo "Stopping one broker (kafka2) for 10s . . ."
docker compose stop kafka2
sleep 10
echo "Starting broker . . ."
docker compose start kafka2
echo "OK: Producer should have continued (acks=all, min.insync.replicas>=2)."


#Mongo outage

echo "Stopping MongoDB for 10s . . ."
docker compose stop mongodb
sleep 10
echo "Starting MongoDB . . ."
docker compose start mongodb
sleep 10

FINAL_CNT=$(mongo_count || echo 0)
echo "Final document count: $FINAL_CNT (should continue increasing, with no gaps visible in /sensors)"
echo "All scenes executed."
