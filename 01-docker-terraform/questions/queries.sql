-- Question 1
--What is the version of pip in the python:3.13 image?

-- Question 2
-- Given the docker-compose.yaml, what is the hostname and port that pgadmin should use to connect to the postgres database? 

select count(*) from green_taxi_data;
select * from green_taxi_data limit 1;

select count(*) from zone_lookup

-- Question 3. Counting short trips
-- For the trips in November 2025, how many trips had a trip_distance of less than or equal to 1 mile?
SELECT COUNT(*) 
FROM green_taxi_data 
WHERE lpep_pickup_datetime BETWEEN '2025-11-01' AND '2025-12-01'
    AND trip_distance <= 1;

-- ans = 8007


-- Question 4. Longest trip for each day
-- Which was the pick up day with the longest trip distance? Only consider trips with trip_distance less than 100 miles.
SELECT
	lpep_pickup_datetime,
	trip_distance
FROM green_taxi_data
WHERE trip_distance < 100
ORDER BY trip_distance DESC
LIMIT 1;

-- ans 2025-11-14


-- Question 5. Biggest pickup zone
-- Which was the pickup zone with the largest total_amount (sum of all trips) on November 18th, 2025? 
WITH amount_per_location AS (
	SELECT 
		"PULocationID",
		DATE("lpep_pickup_datetime"),
		SUM(total_amount) AS amount
	FROM 
		green_taxi_data
	WHERE DATE("lpep_pickup_datetime") = '2025-11-18'
	GROUP BY  1, 2
	ORDER BY 3 DESC
	LIMIT 1
)

SELECT "Zone" 
FROM zone_lookup z
JOIN amount_per_location l
	ON l."PULocationID" = z."LocationID";

-- ans: "East Harlem North"



--Question 6. Largest tip
-- For the passengers picked up in the zone named "East Harlem North" in November 2025,
-- which was the drop off zone that had the largest tip?
WITH trips_east_harlem_north AS (
	SELECT
		"DOLocationID",
		MAX(tip_amount) AS largest_tip
	FROM
		green_taxi_data
	WHERE "PULocationID" = (
		SELECT 
			"LocationID"
		FROM zone_lookup
		WHERE "Zone" = 'East Harlem North'
	)
	GROUP BY "DOLocationID"
	ORDER BY largest_tip DESC
	LIMIT 1
)
SELECT 
	"Zone"
FROM
	zone_lookup
WHERE "LocationID" = (SELECT "DOLocationID" FROM trips_east_harlem_north);

--ans "Yorkville West"


