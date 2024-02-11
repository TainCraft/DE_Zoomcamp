
--external table--
CREATE OR REPLACE EXTERNAL TABLE ny_taxi.external_green_taxi
OPTIONS (
  format="parquet",
  uris = ['gs://mage-zoomcamp-sl2/green/green_tripdata_2022-*.parquet']
);

--partition--
CREATE OR REPLACE TABLE ny_taxi.green_taxi_partitioned
PARTITION BY
  DATE(lpep_pickup_datetime) AS
SELECT * FROM ny_taxi.green_taxi;

select * from ny_taxi.external_green_taxi limit 10;

--Row Count--
select count(*) from `ny_taxi.green_taxi`;

--Amount Normal--
SELECT COUNT(DISTINCT 'PULocationID') AS distinct_pulocationid
FROM ny_taxi.green_taxi;

--Amount External--
SELECT COUNT(DISTINCT 'PULocationID') AS distinct_pulocationid
FROM ny_taxi.external_green_taxi;

--Count rows with zero fare_amount--
SELECT COUNT(*) FROM `ny_taxi.green_taxi` WHERE fare_amount = 0; 

--Amount non-partitioned--
SELECT COUNT(DISTINCT 'PULocationID') AS distinct_pulocationid
FROM ny_taxi.green_taxi
WHERE DATE(lpep_pickup_datetime) BETWEEN '2022-06-01' AND '2022-06-30';

--Amount partitioned--
SELECT COUNT(DISTINCT 'PULocationID') AS distinct_pulocationid
FROM ny_taxi.green_taxi_partitioned
WHERE DATE(lpep_pickup_datetime) BETWEEN '2022-06-01' AND '2022-06-30';

SELECT COUNT(*) FROM 'ny_taxi.green_taxi_partitioned_clustered';