import duckdb

# connect to the DuckDB file created by dlt
con = duckdb.connect("taxi_pipeline.duckdb")

print("=== Question 1: Start and End Date of Dataset ===\n")

result = con.execute("""
SELECT
  MIN(DATE(trip_pickup_date_time)) AS start_date,
  MAX(DATE(trip_pickup_date_time)) AS end_date,
  COUNT(*) AS total_records
FROM taxi_data.yellow_taxi_trips
""").fetchall()

for row in result:
    print(f"Start Date: {row[0]}")
    print(f"End Date: {row[1]}")
    print(f"Total Records: {row[2]}")

print("\n\n=== Question 2: Proportion of trips paid with credit card ===\n")

result = con.execute("""
SELECT
  payment_type,
  COUNT(*) as count,
  ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as percentage
FROM taxi_data.yellow_taxi_trips
GROUP BY payment_type
ORDER BY count DESC
""").fetchall()

total_trips = 0
credit_trips = 0

for payment_type, count, percentage in result:
    print(f"{payment_type}: {count} trips ({percentage}%)")
    total_trips += count
    if payment_type == 'Credit':
        credit_trips = count

print(f"\nTotal trips: {total_trips}")
print(f"Credit trips: {credit_trips}")
credit_percentage = (credit_trips / total_trips) * 100
print(f"\n✓ Credit card percentage: {credit_percentage:.2f}%")

print("\n\n=== Question 3: Total amount of money in tips ===\n")

result = con.execute("""
SELECT
  ROUND(SUM(tip_amt), 2) as total_tips,
  ROUND(AVG(tip_amt), 2) as avg_tip,
  MIN(tip_amt) as min_tip,
  MAX(tip_amt) as max_tip
FROM taxi_data.yellow_taxi_trips
""").fetchall()

for total_tips, avg_tip, min_tip, max_tip in result:
    print(f"Total Tips: ${total_tips:,.2f}")
    print(f"Average Tip: ${avg_tip:.2f}")
    print(f"Min Tip: ${min_tip:.2f}")
    print(f"Max Tip: ${max_tip:.2f}")

con.close()
