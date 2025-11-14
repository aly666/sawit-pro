
Site Reliability Engineer – Log Processing & Observability Assignment

Proyek ini adalah solusi untuk tugas SRE 2025 dari SawitPro.
Tujuannya:

- Menjalankan 3 instance aplikasi yang menghasilkan log melalui STDOUT
- Menangkap log ke file
- Melakukan parsing & convert ke JSONL
- Mengirim ke Loki via Promtail
- Menampilkan dashboard observability di Grafana

Arsitektur

App (3 instances)
    ↓ stdout
raw log files (shared volume)
    ↓
Parser (python)
    ↓
parsed.jsonl
    ↓
Promtail
    ↓
Loki
    ↓
Grafana Dashboard

 Perubahan yang Saya Lakukan
1. Memperbaiki Dockerfile aplikasi

Binary tidak bisa dijalankan karena salah nama (app-linux-amd64 → app)

Dockerfile diperbaiki:
COPY app-linux-amd64 ./app
RUN chmod +x ./app
CMD ["./app"]

2. Memperbaiki docker-compose agar log ditulis ke file

Awalnya STDOUT tidak masuk volume → diperbaiki menjadi:
command: >
  sh -c "while true; do ./app; sleep 0.1; done >> /rawlogs/app1.log 2>&1"
  
4. Membuat Python parser

Parser membaca file .log, mem-parse regex, dan menulis parsed.jsonl.

5. Menambah konfigurasi Promtail

Promtail membaca JSONL dan push ke Loki.

6. Membuat dashboard Grafana lengkap
Dashboard berisi: -->
- Success Rate
- Error Rate
- Latency p50/p90/p99
- RPS
- Error breakdown (404,500)
- Traffic per service
- Version distribution
- Raw logs viewer
- Total 200/404/500 

🚀 Cara Menjalankan
docker-compose up --build

Komponen:
- App berjalan menghasilkan log
- Parser membaca & membuat parsed.jsonl
- Promtail kirim ke Loki
- Grafana dapat diakses di:
  👉 http://localhost:8085
  user: admin / pass: admin

Export Dashboard
grafana-dashboard.json