> cd 02-workflow-orchestration
> docker compose up -d

> docker compose down


SELECT SUM(total_rows) 
FROM (
    SELECT COUNT(*) AS total_rows
    FROM `dtc-de-course-486019.zoomcamp.green_tripdata_2020_01`
    UNION ALL
    SELECT COUNT(*) AS total_rows
    FROM `dtc-de-course-486019.zoomcamp.green_tripdata_2020_02`
    UNION ALL
    SELECT COUNT(*) AS total_rows
    FROM `dtc-de-course-486019.zoomcamp.green_tripdata_2020_03`
    UNION ALL
    SELECT COUNT(*) AS total_rows
    FROM `dtc-de-course-486019.zoomcamp.green_tripdata_2020_04`
    UNION ALL
    SELECT COUNT(*) AS total_rows
    FROM `dtc-de-course-486019.zoomcamp.green_tripdata_2020_05`
    UNION ALL
    SELECT COUNT(*) AS total_rows
    FROM `dtc-de-course-486019.zoomcamp.green_tripdata_2020_06`
    UNION ALL
    SELECT COUNT(*) AS total_rows
    FROM `dtc-de-course-486019.zoomcamp.green_tripdata_2020_07`
    UNION ALL
    SELECT COUNT(*) AS total_rows
    FROM `dtc-de-course-486019.zoomcamp.green_tripdata_2020_08`
    UNION ALL
    SELECT COUNT(*) AS total_rows
    FROM `dtc-de-course-486019.zoomcamp.green_tripdata_2020_09`
    UNION ALL
    SELECT COUNT(*) AS total_rows
    FROM `dtc-de-course-486019.zoomcamp.green_tripdata_2020_10`
    UNION ALL
    SELECT COUNT(*) AS total_rows
    FROM `dtc-de-course-486019.zoomcamp.green_tripdata_2020_11`
    UNION ALL
    SELECT COUNT(*) AS total_rows
    FROM `dtc-de-course-486019.zoomcamp.green_tripdata_2020_12`
) green

