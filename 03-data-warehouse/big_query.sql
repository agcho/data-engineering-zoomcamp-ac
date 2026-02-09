
--Create an external table using the Yellow Taxi Trip Records.
CREATE OR REPLACE EXTERNAL TABLE `dtc-de-course-486019.zoomcamp.yellow_taxi_2024_external`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://kestra-zoomcamp-ac-hw3/yellow_tripdata_2024-*.parquet']
);

--Create a (regular/materialized) table in BQ using the Yellow Taxi Trip Records (do not partition or cluster this table).
CREATE OR REPLACE TABLE `dtc-de-course-486019.zoomcamp.yellow_taxi_2024_regular` AS
SELECT *
FROM `dtc-de-course-486019.zoomcamp.yellow_taxi_2024_external`;

--Q1. What is count of records for the 2024 Yellow Taxi Data?
SELECT COUNT(Vendor ID) FROM `dtc-de-course-486019.zoomcamp.yellow_taxi_2024_external`;
SELECT COUNT(Vendor ID) FROM `dtc-de-course-486019.zoomcamp.yellow_taxi_2024_regular`;

--Q2. Write a query to count the distinct number of PULocationIDs for the entire dataset on both the tables.
--    What is the estimated amount of data that will be read when this query is executed on the External Table and the Table?
SELECT PULocationID
FROM `dtc-de-course-486019.zoomcamp.yellow_taxi_2024_regular`;

SELECT PULocationID, DOLocationID
FROM `dtc-de-course-486019.zoomcamp.yellow_taxi_2024_regular`;

--Q4. How many records have a fare_amount of 0? (1 point)
SELECT count(*)
FROM `dtc-de-course-486019.zoomcamp.yellow_taxi_2024_regular`
WHERE fare_amount = 0;


--Q5. What is the best strategy to make an optimized table in Big Query if your query will always filter based on tpep_dropoff_datetime and order the results by VendorID (Create a new table with this strategy)
CREATE OR REPLACE TABLE `dtc-de-course-486019.zoomcamp.yellow_taxi_2024_optimized`
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID AS
SELECT *
FROM `dtc-de-course-486019.zoomcamp.yellow_taxi_2024_regular`;

--Q6. Write a query to retrieve the distinct VendorIDs between tpep_dropoff_datetime 2024-03-01 and 2024-03-15 (inclusive). Use the materialized table you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the partitioned table you created for question 5 and note the estimated bytes processed. What are these values? (1 point)
SELECT DISTINCT VendorID
FROM `dtc-de-course-486019.zoomcamp.yellow_taxi_2024_regular`
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15';

SELECT DISTINCT VendorID
FROM `dtc-de-course-486019.zoomcamp.yellow_taxi_2024_optimized`
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15';

