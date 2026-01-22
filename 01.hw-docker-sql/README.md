# Dockerized PostgreSQL Ingestion Pipeline

### Overview
This project demonstrates an end-to-end data ingestion workflow using Docker and Docker Compose.
The goal is to load NYC taxi datasets into PostgreSQL, explore them, and query them using pgAdmin.

- Start with a database stack, creating containers for Postgres and pgAdming from docker-compose.
- Explore data locally using a notebook.
- Convert exploration into a script.
- Containerize ingestion as a batch job


### Architecture
The project uses three containers, each with a clear responsibility:

- **PostgreSQL**: 
Stores the ingested data and uses a Docker volume for persistence.

- **pgAdmin**: 
Web UI for querying and inspecting the database, accessed from the browser on the host machine.

- **Ingestion container**: 
Runs a Python script as a one-off batch job: loads data into PostgreSQL and exits.

### Workflow
The workflow mirrors a realistic data engineering process:

1. Database Stack (Docker Compose)

The database stack is started first:

```
docker compose up -d
```

This launches:

- PostgreSQL on port 5432
- pgAdmin on port 8080

pgAdmin is accessed in the browser to inspect tables and run SQL queries.

2. Data Exploration (Local, Notebook)
Before ingestion, the datasets are explored locally using a Jupyter notebook:

- Inspect schema
- Check row counts
- Decide whether chunking is necessary

This helps keep the ingestion script simple.

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

For simplicity, the `data/` folder is mounted into the ingestion container.

In a production setup, the container would:
- Download data at runtime if local, or
- Read from object storage


### Accessing the Database
The database is accessed via pgAdmin in the browser:
- URL: `http://localhost:8080`
- Host: `pgdatabase`
- Port: `5432`
- Database: `ny_taxi`

*All SQL queries for the assignment are executed through pgAdmin.*

### Key Learnings
- Docker Compose simplifies multi-container setups
- Batch ingestion containers should exit after completion
- Data exploration before ingestion reduces complexity
- Volumes persist data independently of containers
- Service names act as hostnames inside Docker networks

### Future Improvements
- Download data inside the ingestion container
- Add basic data validation
- Parameterize dataset selection (year/month) for full dataset
- Add logging instead of print statements


