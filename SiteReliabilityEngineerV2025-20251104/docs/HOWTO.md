# HOWTO: Menjalankan Project 

## Prasyarat
Docker
Docker Compose
Port:
    - 8085 (Grafana)
    - 3100 (Loki)
## Menjalankan semua service
docker-compose up --build

Cek apakah log berjalan

A. Raw log
ls logs/raw
B. Parsed JSON
tail -f logs/parsed/parsed.jsonl

## Akses Grafana
http://localhost:8085
Username: admin
Password: admin
Import dashboard → Upload file:
grafana-dashboard.json

Query Loki contoh
Total request:
sum(rate({job="parsed-json"} | json [1m]))
Error 404:
sum(rate({job="parsed-json"} | json | status_code=404 [1m]))
Latency p90:
quantile_over_time(0.90, {job="parsed-json"} | json | unwrap response_time_ms [5m])

## Stop seluruh service
docker-compose down
