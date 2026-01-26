import time
import click
import pandas as pd
from sqlalchemy import create_engine


@click.command()
@click.option('--pg-user', default='postgres', help='PostgreSQL user')
@click.option('--pg-pass', default='postgres', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default=5433, type=int, help='PostgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database name')
@click.option('--target-table', default='green_taxi_2025_11', help='Target table name')
@click.option('--year', default=2025, type=int, help='Year of the dataset')
@click.option('--month', default=11, type=int, help='Month of the dataset')
@click.option('--chunksize', default=100_000, type=int, help='Rows per batch when writing to Postgres')

def run(pg_user, pg_pass, pg_host, pg_port, pg_db, target_table, year, month, chunksize):
    """
    Ingest a Parquet green taxi dataset into Postgres in chunks.
    """
    start_time = time.time()

    prefix = 'https://d37ci6vzurychx.cloudfront.net/trip-data/'
    url = f'{prefix}green_tripdata_{year:04d}-{month:02d}.parquet'
    print(f"\n Reading Parquet from: {url}")

    engine = create_engine(
        f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}'
    )
    print(f"🔌 Connecting to Postgres: postgresql://{pg_user}:***@{pg_host}:{pg_port}/{pg_db}")

    df = pd.read_parquet(url)
    print(f" Loaded {len(df):,} rows")
    print(" Columns:", df.columns.tolist())

    # Optional: sanitize datetime columns (parquet usually already handles this)
    for col in df.columns:
        lc = col.lower()
        if 'datetime' in lc or 'pickup' in lc or 'dropoff' in lc:
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

    print(f"\n Writing to Postgres table '{target_table}' in chunks of {chunksize:,} rows...")

    df.to_sql(
        name=target_table,
        con=engine,
        if_exists='replace',
        index=False,
        chunksize=chunksize,
        method='multi',
    )

    elapsed = time.time() - start_time
    print(f"\n Done! Loaded {len(df):,} rows into '{target_table}' in {elapsed:.1f} seconds.\n")


if __name__ == '__main__':
    run()
