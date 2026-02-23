"""@bruin

name: ingestion.trips
type: python
image: python:3.11

connection: duckdb-default

materialization:
  type: table
  strategy: append

@bruin"""

import os
import json
import pandas as pd
import requests
from datetime import datetime, timedelta, timezone
from io import BytesIO

def materialize():
    # Get date range from environment
    start_date_str = os.environ.get('BRUIN_START_DATE')
    end_date_str = os.environ.get('BRUIN_END_DATE')
    
    if not start_date_str or not end_date_str:
        raise ValueError("BRUIN_START_DATE and BRUIN_END_DATE must be set")
    
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    
    # Get pipeline variables
    bruin_vars = os.environ.get('BRUIN_VARS', '{}')
    vars_dict = json.loads(bruin_vars)
    taxi_types = vars_dict.get('taxi_types', ['yellow'])
    
    # Generate list of months to download
    months = []
    current = start_date.replace(day=1)
    while current <= end_date:
        months.append((current.year, current.month))
        # Move to next month
        if current.month == 12:
            current = current.replace(year=current.year + 1, month=1)
        else:
            current = current.replace(month=current.month + 1)
    
    # Base URL for NYC TLC data
    base_url = 'https://d37ci6vzurychx.cloudfront.net/trip-data/'
    
    all_dataframes = []
    
    for taxi_type in taxi_types:
        for year, month in months:
            file_name = f"{taxi_type}_tripdata_{year}-{month:02d}.parquet"
            url = f"{base_url}{file_name}"
            
            print(f"Downloading {url}")
            try:
                response = requests.get(url)
                response.raise_for_status()
                
                # Read Parquet from bytes
                df = pd.read_parquet(BytesIO(response.content))
                
                # Convert timestamp columns to UTC timezone
                timestamp_cols = ['tpep_pickup_datetime', 'tpep_dropoff_datetime']
                for col in timestamp_cols:
                    if col in df.columns:
                        df[col] = pd.to_datetime(df[col]).dt.tz_localize('UTC')
                
                # Add metadata columns
                df['taxi_type'] = taxi_type
                df['extracted_at'] = datetime.now(timezone.utc)
                
                all_dataframes.append(df)
                print(f"Loaded {len(df)} rows for {taxi_type} {year}-{month:02d}")
                
            except requests.exceptions.RequestException as e:
                print(f"Failed to download {url}: {e}")
                continue
    
    if not all_dataframes:
        # Return empty dataframe with expected columns if no data
        return pd.DataFrame()
    
    # Concatenate all dataframes
    final_df = pd.concat(all_dataframes, ignore_index=True)
    
    return final_df


