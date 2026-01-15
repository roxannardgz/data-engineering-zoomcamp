import click
import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm


# Explicit typing to help pandas parse consistently
# Note: pandas nullable "Int64" allows NULLs.
DTYPE = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64",
}

PARSE_DATES = ["tpep_pickup_datetime", "tpep_dropoff_datetime"]


def ingest_data(
    url: str,
    engine,
    target_table: str,
    read_chunksize: int = 100_000,
    write_chunksize: int = 10_000,
) -> None:

    """
    Stream a gzipped CSV from URL and load into Postgres in chunks.

    Args:
        url: CSV/CSV.GZ URL or local path.
        engine: SQLAlchemy engine.
        target_table: Destination table name.
        read_chunksize: Rows per pandas read chunk.
        write_chunksize: Rows per SQL insert batch.
    """
    # Create an iterator over chunks to avoid loading everything into RAM
    df_iter = pd.read_csv(
        url,
        dtype=DTYPE,
        parse_dates=PARSE_DATES,
        iterator=True,
        chunksize=read_chunksize,
    )

    first_chunk = next(df_iter)

    # Create/replace table schema (no rows)
    first_chunk.head(0).to_sql(
        name=target_table,
        con=engine,
        if_exists="replace",
        index=False
    )

    # Insert first chunk
    first_chunk.to_sql(
        name=target_table,
        con=engine,
        if_exists="append",
        index=False,
        method="multi",
        chunksize=write_chunksize,
        )

    total_rows = len(first_chunk)

    # Insert remaining chunks with progress bar
    for df_chunk in tqdm(df_iter, desc=f"Loading {target_table}"):
        df_chunk.to_sql(
            name=target_table,
            con=engine,
            if_exists="append",
            index=False,
            method="multi",
            chunksize=write_chunksize,
        )
        total_rows += len(df_chunk)

    print(f"Done. Loaded {total_rows:,} rows into '{target_table}'.")


@click.command()
@click.option("--pg-user", default="root", show_default=True)
@click.option("--pg-pass", default="root", show_default=True)
@click.option("--pg-host", default="localhost", show_default=True)
@click.option("--pg-port", default="5432", show_default=True)
@click.option("--pg-db", default="ny_taxi", show_default=True)
@click.option("--year", type=int, default=2021, show_default=True)
@click.option("--month", type=int, default=1, show_default=True)
@click.option("--read-chunksize", type=int, default=100_000, show_default=True)
@click.option("--write-chunksize", type=int, default=10_000, show_default=True)
@click.option("--target-table", default="yellow_taxi_data", show_default=True)
def main(
    pg_user: str,
    pg_pass: str,
    pg_host: str,
    pg_port: str,
    pg_db: str,
    year: int,
    month: int,
    read_chunksize: int,
    write_chunksize: int,
    target_table: str,
) -> None:

    engine = create_engine(
        f"postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}"
    )

    url_prefix = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow"
    url = f"{url_prefix}/yellow_tripdata_{year:04d}-{month:02d}.csv.gz"

    ingest_data(
        url=url,
        engine=engine,
        target_table=target_table,
        read_chunksize=read_chunksize,
        write_chunksize=write_chunksize
    )


if __name__ == "__main__":
    main()
