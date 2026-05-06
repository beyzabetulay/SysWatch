<p align="center">
  <h1 align="center">🖥️ SysWatch</h1>
  <p align="center">
    <strong>A lightweight, real-time system monitoring toolkit built with Python.</strong>
  </p>
  <p align="center">
    Collect · Analyze · Visualize · Alert
  </p>
  <p align="center">
    <a href="#-features">Features</a> •
    <a href="#-architecture">Architecture</a> •
    <a href="#-quick-start">Quick Start</a> •
    <a href="#-api-reference">API Reference</a> •
    <a href="#-visualization">Visualization</a> •
    <a href="#-tech-stack">Tech Stack</a>
  </p>


---

## 📖 About

SysWatch continuously monitors your machine's CPU, memory, disk and network metrics, persists them to a database, exposes them through a REST API, and provides both real-time and static visualization dashboards. It is fully containerized with Docker for effortless deployment.

---

## ✨ Features

| Category | Description |
|---|---|
| **Real-Time Monitoring** | Collects CPU %, RAM %, disk usage, and network I/O every N seconds using `psutil`. |
| **Process Tracker** | Identifies the top N most resource-hungry processes on the system. |
| **REST API** | FastAPI-powered endpoints for live metrics, historical queries, spike alerts, and summary statistics. |
| **Data Persistence** | Dual storage: append-only CSV files for portability and SQLite + SQLAlchemy ORM for structured queries. |
| **Database Migrations** | Schema versioning and migrations managed with Alembic. |
| **Trend Analysis** | Pandas-based analysis engine with spike detection, rolling averages, and JSON report export. |
| **Live Dashboard** | Real-time animated Matplotlib chart showing CPU and RAM over time. |
| **Static Reports** | Generates a 2×2 PNG dashboard (line charts, bar chart, histogram) from collected data. |
| **Rotating Logs** | Structured logging with automatic file rotation (5 MB cap, 3 backups). |
| **Dockerized** | Single-command deployment via `docker-compose` with host PID namespace for accurate host metrics. |

---

## 🏗️ Architecture

```text
SysWatch/
│
├── monitor/                 # Core data-collection layer
│   ├── system_reader.py     # Reads CPU, RAM, disk & network via psutil
│   ├── process_monitor.py   # Top-N process tracker by CPU usage
│   ├── scheduler.py         # Timed collection loop with graceful shutdown
│   ├── csv_writer.py        # Thread-safe CSV append writer
│   └── logger.py            # Rotating file + stream logger setup
│
├── api/                     # REST API layer
│   └── main.py              # FastAPI app with all endpoint definitions
│
├── database/                # Persistence layer
│   ├── models.py            # SQLAlchemy ORM models & query helpers
│   └── __init__.py
│
├── analysis/                # Data analysis layer
│   └── trends.py            # Pandas trend analysis & spike detection
│
├── visualize/               # Visualization layer
│   ├── live_chart.py        # Real-time animated Matplotlib dashboard
│   └── report.py            # Static 2×2 PNG report generator
│
├── alembic/                 # Database migration scripts
│   └── env.py               # Alembic environment configuration
├── alembic.ini              # Alembic settings
│
├── data/                    # Runtime data (CSV + SQLite DB)
├── logs/                    # Rotating log files
├── reports/                 # Generated PNG reports
│
├── Dockerfile               # Container image definition
├── docker-compose.yml       # Orchestration config
├── requirements.txt         # Python dependencies
└── README.md
```

### Data Flow

```
psutil (host) → system_reader → scheduler ─┬─→ csv_writer  → data/metrics.csv
                                            ├─→ database    → data/syswatch.db
                                            └─→ logger      → logs/syswatch.log
                                                    │
                            FastAPI ← database ←────┘
                                │
                        localhost:8001/docs
```

---

## 🚀 Quick Start

### Option 1 — Docker (Recommended)

The fastest way to get up and running. The container uses `pid: "host"` so `psutil` reports the **host machine's** actual metrics, not the container's.

```bash
# Clone the repository
git clone https://github.com/beyzabetulay/SysWatch.git
cd SysWatch

# Build and start
docker-compose up --build
```

The API will be available at **http://localhost:8001**.

### Option 2 — Local Development

```bash
# Create a virtual environment
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate    # Windows

# Install dependencies
pip install -r requirements.txt

# Start the API server
uvicorn api.main:app --host 0.0.0.0 --port 8001 --reload

# (In a separate terminal) Start the background metric collector
python -m monitor.scheduler
```

---

## 📡 API Reference

Once the server is running, interactive docs are auto-generated:

- **Swagger UI:** [http://localhost:8001/docs](http://localhost:8001/docs)
- **ReDoc:** [http://localhost:8001/redoc](http://localhost:8001/redoc)

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/metrics/current` | Returns a live snapshot of CPU, RAM, disk and network stats. |
| `GET` | `/metrics/history?last_minutes=60` | Retrieves stored metric records from the last N minutes. |
| `GET` | `/metrics/alerts?cpu_threshold=80` | Lists all recorded snapshots where CPU exceeded the given threshold. |
| `GET` | `/metrics/summary?last_minutes=60` | Returns aggregate statistics (avg CPU, max CPU, spike count) for the period. |

### Example Response — `/metrics/current`

```json
{
  "timestamp": "2026-05-06 21:30:12",
  "cpu_usage - %": 23.5,
  "memory_usage_percent - %": 61.2,
  "memory_usage_total - GB": 15.52,
  "memory_usage_free - GB": 5.98,
  "memory_usage_used - GB": 9.54,
  "disk_usage_percent - %": 47.8,
  "disk_usage_total - GB": 476.94,
  "disk_usage_free - GB": 248.95,
  "disk_usage_used - GB": 203.65,
  "net_io_sent - MB": 1024.33,
  "net_io_recv - MB": 4892.17
}
```

---

## 📊 Visualization

### Live Dashboard

A real-time animated Matplotlib window showing the last 60 seconds of CPU and RAM usage. Includes a configurable warning threshold line.

```bash
python -m visualize.live_chart
```

### Static Report

Generates a `reports/report.png` dashboard with four panels:

- **CPU Usage Over Time** — line chart
- **RAM Usage Over Time** — line chart
- **Memory Distribution** — bar chart (free vs. used GB)
- **CPU Usage Distribution** — histogram

```bash
python -m visualize.report
```

---

## 🔧 Additional Tools

### Background Scheduler

Runs in an infinite loop, collecting snapshots at a configurable interval, writing to CSV and logging. Supports graceful shutdown with `Ctrl+C`.

```bash
python -m monitor.scheduler
```

### Trend Analysis

Performs spike detection and generates a JSON analysis report from the collected CSV data.

```bash
python -m analysis.trends
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Monitoring | [psutil](https://github.com/giampaolo/psutil) |
| API | [FastAPI](https://fastapi.tiangolo.com/) + [Uvicorn](https://www.uvicorn.org/) |
| ORM & Database | [SQLAlchemy](https://www.sqlalchemy.org/) + SQLite |
| Migrations | [Alembic](https://alembic.sqlalchemy.org/) |
| Analysis | [Pandas](https://pandas.pydata.org/) |
| Visualization | [Matplotlib](https://matplotlib.org/) |
| Containerization | [Docker](https://www.docker.com/) + Docker Compose |

---

## 📄 License

This project is for educational and personal use.

---
