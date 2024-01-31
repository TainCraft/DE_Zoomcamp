Question 3:
SELECT count(1)
FROM green_taxi_trips
WHERE lpep_pickup_date = '2019-09-18'
  AND lpep_dropoff_date= '2019-09-18';





Question 4:
SELECT 
    lpep_pickup_date AS pickup_day,
    MAX(lpep_dropoff_time - lpep_pickup_time) AS longest_trip_duration
FROM green_taxi_trips
GROUP BY pickup_day
ORDER BY longest_trip_duration DESC
LIMIT 1;





Question 5:
SELECT 
    pickup_borough,
    SUM(total_amount) AS total_amount_sum
FROM (
    SELECT
        gt.*,
        tz."Borough" AS pickup_borough
    FROM green_taxi_trips gt
    JOIN taxi_lookup_zone tz ON gt."PULocationID" = tz."LocationID"
) AS trips_with_borough
WHERE trips_with_borough."lpep_pickup_date" = '2019-09-18'
    AND pickup_borough NOT IN ('Unknown')
GROUP BY pickup_borough
HAVING SUM(total_amount) > 50000
ORDER BY total_amount_sum DESC
LIMIT 3;





Question 6:
SELECT
    tz_dropoff."Zone" AS dropoff_zone,
    MAX(gtt."tip_amount") AS max_tip_amount
FROM
    green_taxi_trips gtt
JOIN
    taxi_lookup_zone tz_pickup ON gtt."PULocationID" = tz_pickup."LocationID"
JOIN
    taxi_lookup_zone tz_dropoff ON gtt."DOLocationID" = tz_dropoff."LocationID"
WHERE
    tz_pickup."Zone" = 'Astoria'
    AND DATE_TRUNC('month', gtt."lpep_pickup_date") = '2019-09-01'
GROUP BY
    tz_dropoff."Zone"
ORDER BY
    max_tip_amount DESC
LIMIT 1;
