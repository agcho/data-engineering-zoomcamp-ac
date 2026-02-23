Question 1. Bruin Pipeline StructureIn a Bruin project, what are the required files/directories? (1 point)

> .bruin.yml and pipeline/ with pipeline.yml and assets/

Question 2. Materialization Strategies You're building a pipeline that processes NYC taxi data organized by month based on pickup_datetime. Which incremental strategy is best for processing a specific interval period by deleting and inserting data for that time period? (1 point)

> time_interval - incremental based on a time column

Question 3. Pipeline VariablesYou have a variable defined in pipeline.yml:variables: taxi_types: type: array items: type: string default: ["yellow", "green"]How do you override this when running the pipeline to only process yellow taxis? (1 point)

> bruin run --var 'taxi_types=["yellow"]'

Question 4. Running with DependenciesYou've modified the ingestion/trips.py asset and want to run it plus all downstream assets. Which command should you use? (1 point)

> bruin run ingestion/trips.py --downstream

Question 5. Quality Checks. You want to ensure the pickup_datetime column in your trips table never has NULL values. Which quality check should you add to your asset definition? (1 point)

> name: not_null

Question 6. Lineage and DependenciesAfter building your pipeline, you want to visualize the dependency graph between assets. Which Bruin command should you use? (1 point)

> bruin lineage

Question 7. Question 7. First-Time RunYou're running a Bruin pipeline for the first time on a new DuckDB database. What flag should you use to ensure tables are created from scratch? (1 point)

> --full-refresh