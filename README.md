# Surf Forecasting Pipeline

A full production-style data pipeline that ingests marine, weather, and tide forecast data for NJ surf breaks, transforms it through a layered data model, and prepares features for ML-based surf quality prediction.

Built as a hands-on project to learn production data engineering patterns: Docker, Airflow orchestration, dbt transformations, and cloud deployment.

## Architecture

```
Open-Meteo Marine API ─┐
Open-Meteo Weather API ─┼─→ Airflow DAG ─→ PostgreSQL (raw) ─→ dbt ─→ PostgreSQL (gold)
NOAA CO-OPS Tide API  ──┘
```

**Ingest** — Python scripts pull hourly forecasts from three independent APIs and write to raw PostgreSQL tables. Each source is fetched and stored independently so a failure in one doesn't block the others.

**Transform** — dbt models organized in three layers:
- **Staging** — Unit conversions (meters → feet, Celsius → Fahrenheit, km/h → mph), type casting
- **Intermediate** — Feature engineering: swell-to-wind-wave ratio, circular encoding of wind/swell directions, cardinal direction labels, tide change rate
- **Gold** — Joined fact table combining marine, weather, and tide data with deduplication to keep only the most recent forecast per hour

**Orchestration** — Airflow runs the full pipeline daily: ingest first, then dbt build (models + tests). Task dependencies ensure transforms only run after successful ingestion.

**Infrastructure** — Everything runs in Docker Compose on a DigitalOcean Droplet: two PostgreSQL instances (Airflow metadata + application data), Airflow webserver, and Airflow scheduler.

## Data Sources

| Source | API | Data | Frequency |
|--------|-----|------|-----------|
| Open-Meteo Marine | `marine-api.open-meteo.com/v1/marine` | Wave height, swell height/period/direction, wind wave height | 7-day hourly forecast |
| Open-Meteo Weather | `api.open-meteo.com/v1/forecast` | Temperature, wind speed/direction/gusts | 7-day hourly forecast |
| NOAA CO-OPS | `api.tidesandcurrents.noaa.gov` | Tide height predictions | 7-day hourly predictions |

## Surf Breaks

| Break | Location | Tide Station |
|-------|----------|-------------|
| Deal, NJ | 40.19°N, 74.03°W | Sandy Hook (8531680) |
| Belmar, NJ | 40.19°N, 74.03°W | Sandy Hook (8531680) |
| Spring Lake, NJ | 40.15°N, 74.03°W | Sandy Hook (8531680) |

## Project Structure

```
surf-forecaster/
├── dags/
│   └── ingest_dag.py              # Airflow DAG: ingest → dbt build
├── src/
│   ├── main_ingest.py             # Orchestrates fetch → prepare → write
│   └── ingest/
│       ├── marine.py              # Open-Meteo Marine API fetch + prepare
│       ├── weather.py             # Open-Meteo Weather API fetch + prepare
│       ├── tides.py               # NOAA CO-OPS API fetch + prepare
│       └── db.py                  # PostgreSQL connection + write utilities
├── dbt_surf_forecaster/
│   ├── dbt_project.yml
│   ├── profiles.yml               # Production profile (env var credentials)
│   └── models/
│       ├── staging/               # Unit conversions, type casting
│       ├── intermediate/          # Feature engineering
│       └── gold/                  # Joined fact table
├── config/
│   └── breaks.yaml                # Surf break coordinates + tide station IDs
├── sql/
│   └── init.sql                   # Database and schema creation
├── Dockerfile
├── docker-compose.yaml
├── requirements.txt
└── .env.example                   # Template for environment variables
```

## Engineered Features

The transform layer engineers several features from raw forecast data:

- **Swell ratio** — Proportion of total wave height that is clean swell vs wind chop. Higher ratio indicates cleaner, more surfable conditions.
- **Circular direction encoding** — Wind and swell directions converted from degrees to sine/cosine pairs to preserve the circular relationship (359° and 1° are neighbors, not 358° apart).
- **Cardinal directions** — 16-point compass labels (N, NNE, NE, etc.) for human-readable interpretation of wind and swell directions.
- **Tide change rate** — Hour-over-hour change in tide height, indicating whether the tide is rising or falling and how quickly.

## Setup

### Prerequisites
- Docker and Docker Compose
- Python 3.11+
- A PostgreSQL client (DBeaver recommended) for inspecting data

### Local Development

```bash
git clone https://github.com/loupill/surf-forecaster.git
cd surf-forecaster
cp .env.example .env
# Edit .env with your database credentials
```

### Deploy to a Server

```bash
ssh root@your_server_ip
git clone https://github.com/loupill/surf-forecaster.git
cd surf-forecaster
nano .env  # Add your credentials
docker compose up airflow-init
docker compose up -d
```

Access the Airflow UI at `http://your_server_ip:8081` (admin/admin).

## Tech Stack

- **Python** — API ingestion, data preparation
- **PostgreSQL** — Data storage (raw and transformed layers)
- **dbt** — SQL-based data transformation with testing
- **Apache Airflow** — Workflow orchestration and scheduling
- **Docker / Docker Compose** — Containerization and service management
- **DigitalOcean** — Cloud hosting

## What's Next

- Train an ML model (gradient boosting) on the gold layer to predict a surfability score
- Add batch inference to score upcoming forecast days
- Integrate the model training and inference steps into the Airflow DAG
