-- Creating external table referring to gcs path
CREATE OR REPLACE EXTERNAL TABLE `dtc-de-course-486019.nytaxi.external_yellow_tripdata`
OPTIONS (
  format = 'CSV',
  uris = ['gs://kestra-zoomcamp-ac-demo/yellow_tripdata_2019-*.csv', 'gs://kestra-zoomcamp-ac-demo/yellow_tripdata_2020-*.csv']
);

CREATE OR REPLACE EXTERNAL TABLE `dtc-de-course-486019.nytaxi.external_green_tripdata`
OPTIONS (
  format = 'CSV',
  uris = ['gs://kestra-zoomcamp-ac-demo/green_tripdata_2019-*.csv', 'gs://kestra-zoomcamp-ac-demo/green_tripdata_2020-*.csv']
);

CREATE OR REPLACE EXTERNAL TABLE `dtc-de-course-486019.nytaxi.external_fhv_tripdata`
OPTIONS (
  format = 'CSV',
  uris = ['gs://kestra-zoomcamp-ac-demo/fhv_tripdata_2019-*.csv']
);

-- Create a non partitioned table from external table
CREATE OR REPLACE TABLE dtc-de-course-486019.nytaxi.green_tripdata AS
SELECT * FROM dtc-de-course-486019.nytaxi.external_green_tripdata;

CREATE OR REPLACE TABLE dtc-de-course-486019.nytaxi.yellow_tripdata AS
SELECT * FROM dtc-de-course-486019.nytaxi.external_yellow_tripdata;

CREATE OR REPLACE TABLE dtc-de-course-486019.nytaxi.fhv_tripdata AS
SELECT * FROM dtc-de-course-486019.nytaxi.external_fhv_tripdata;

-- Create a partitioned table from external table
CREATE OR REPLACE TABLE dtc-de-course-486019.nytaxi.green_tripdata_partitioned
PARTITION BY
  DATE(lpep_pickup_datetime) AS
SELECT * FROM dtc-de-course-486019.nytaxi.external_green_tripdata;

CREATE OR REPLACE TABLE dtc-de-course-486019.nytaxi.yellow_tripdata_partitioned
PARTITION BY
  DATE(tpep_pickup_datetime) AS
SELECT * FROM dtc-de-course-486019.nytaxi.external_yellow_tripdata;

-- Create a staging table with selected fields and some transformations
CREATE OR REPLACE TABLE dtc-de-course-486019.dbt_prod.stg_fhv_tripdata AS
SELECT
    -- identifiers
    dispatching_base_num,
    affiliated_base_number,

    -- timestamps
    pickup_datetime,
    dropoff_datetime,

    -- rename location fields
    PUlocationID AS pickup_location_id,
    DOlocationID AS dropoff_location_id,

    -- optional field (if exists)
    SR_Flag AS sr_flag
FROM  dtc-de-course-486019.nytaxi.fhv_tripdata
WHERE dispatching_base_num IS NOT NULL;

SELECT count(*) FROM dtc-de-course-486019.dbt_prod.stg_fhv_tripdata;