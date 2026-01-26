import click
import requests
import pandas as pd
from urllib.parse import urlparse
from pathlib import Path
from sqlalchemy import create_engine


def ingest_data(
    url_data: str,
    url_lookup: str,
    engine,
    target_table: str,
    lookup_table: str,
) -> None:

    trips = pd.read_parquet(url_data)
    lookups = pd.read_csv(url_lookup)

    # Create the table taxi_trips from the parquet
    trips.to_sql(
        name=target_table,
        con=engine,
        if_exists="replace",
        index=False
    )

    print(f"Loaded {len(trips):,} rows into '{target_table}'.")

    # Create the table taxi_zones. No need to load in chunks.
    lookups.to_sql(
        name=lookup_table,
        con=engine,
        if_exists="replace",
        index=False
    )

    print(f"Loaded {len(lookups):,} rows into '{lookup_table}'.")



@click.command()
@click.option("--pg-user", default="root", show_default=True)
@click.option("--pg-pass", default="root", show_default=True)
@click.option("--pg-host", default="localhost", show_default=True)
@click.option("--pg-port", default="5432", show_default=True)
@click.option("--pg-db", default="ny_taxi", show_default=True)
@click.option("--target-table", default="green_taxi_data", show_default=True)
@click.option("--lookup-table", default="zone_lookup", show_default=True)

def main(
    pg_user: str,
    pg_pass: str,
    pg_host: str,
    pg_port: str,
    pg_db: str,
    target_table: str,
    lookup_table: str,
) -> None:
    
    # Create engine to connect to the database
    engine = create_engine(f"postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}")


    # URLs for the data files
    green_taxi_url = "data/green_tripdata_2025-11.parquet"
    lookups_url = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv"


    ingest_data(
        url_data=green_taxi_url,
        url_lookup=lookups_url,
        engine=engine,
        target_table=target_table,
        lookup_table=lookup_table,
    )

if __name__ == "__main__":
    main()
