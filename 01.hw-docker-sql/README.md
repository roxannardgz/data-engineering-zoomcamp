# Module 1 Homework: Docker & SQL


## Dockerized PostgreSQL Ingestion Pipeline

### Overview
This project demonstrates an end-to-end data ingestion workflow using Docker and Docker Compose.
The goal is to load NYC taxi datasets into PostgreSQL, explore them, and query them using pgAdmin.

The workflow intentionally mirrors a realistic data engineering process:
Start with a database stack
Explore data locally
Convert exploration into a script
Containerize ingestion as a batch job


### Architecture
The project uses three containers, each with a clear responsibility:

**PostgreSQL**
Stores the ingested data
Uses a Docker volume for persistence

**pgAdmin**
Web UI for querying and inspecting the database
Accessed from the browser on the host machine

**Ingestion container**
Runs a Python script as a one-off batch job
Loads data into PostgreSQL and exits

Workflow
1. Database Stack (Docker Compose)

The database stack is started first:

```
docker compose up -d
```


This launches:

- PostgreSQL on port 5432
- pgAdmin on port 8080

pgAdmin is accessed in the browser to inspect tables and run SQL queries.

2. Data Exploration (Local)

Before ingestion, the datasets are explored locally using a Jupyter notebook:

- Inspect schema
- Check row counts
- Decide whether chunking is necessary

This helps keep the ingestion script simple and intentional.

3. Ingestion Script

The ingestion logic is implemented in main.py:

- Reads taxi trip data (Parquet)
- Reads zone lookup data (CSV)
- Loads both into PostgreSQL using SQLAlchemy
- Uses Click for CLI parameters

Because the datasets are small, they are loaded without chunking.

4. Containerized Ingestion

The ingestion script is containerized using a Dockerfile:

- Uses python:3.13-slim
- Installs dependencies with uv sync --locked
- Runs the script as the container entrypoint
- The container is executed as a job, not a long-running service:

```
docker run --rm \
  --network 01hw-docker-sql_default \
  taxi_ingest \
  --pg-host pgdatabase \
  --pg-port 5432
```

After successful ingestion, the container exits.

### Data Handling Note

For simplicity in this version:
- The data/ folder is mounted into the ingestion container
- This avoids rebuilding the image during development

In a production setup, the container would:
- Download data at runtime, or
- Read from object storage (e.g. S3)

This trade-off is documented intentionally.

### Accessing the Database

- The database is accessed via pgAdmin in the browser:
- URL: http://localhost:8080
- Host: pgdatabase
- Port: 5432
- Database: ny_taxi

All SQL queries for the assignment are executed through pgAdmin.

### Key Learnings
- Docker Compose simplifies multi-container setups
- Batch ingestion containers should exit after completion
- Data exploration before ingestion reduces complexity
- Volumes persist data independently of containers
- Service names act as hostnames inside Docker networks

### Future Improvements
- Download data inside the ingestion container
- Add basic data validation
- Parameterize dataset selection (year/month)
- Add logging instead of print statements



### Q1
**What's the version of pip in the image?**<br>
Run docker with the python:3.13 image. Use an entrypoint bash to interact with the container.

--> **25.3**

```
docker run -it --entrypoint bash python:3.13
```

Done directly with `docker run` in interactive mode and overriding the eßntrypoint. In this case it is more convenient than creating a Dockerfile, since it is not intended for repeatable work.

### Q2.



