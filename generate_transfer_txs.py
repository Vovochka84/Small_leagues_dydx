from google.cloud import bigquery
from google.oauth2 import service_account
import csv
import os

# Set up credentials
credentials = service_account.Credentials.from_service_account_file(
    "credentials.json",
    scopes=["https://www.googleapis.com/auth/cloud-platform"],
)

# Initialize BigQuery client
client = bigquery.Client(credentials=credentials, project=credentials.project_id)

# SQL query
query = """
SELECT * FROM `numia-data.dydx_mainnet.dydx_withdrawal`
WHERE sender <> recipient
"""

# Run the query
query_job = client.query(query)

# Get the results
results = query_job.result()

# Prepare CSV file
csv_filename = "transfer_txs.csv"

# Write results to CSV
with open(csv_filename, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)

    # Write header
    writer.writerow([field.name for field in results.schema])

    # Write data rows
    for row in results:
        writer.writerow(row.values())

print(f"Query results saved to {csv_filename}")

# Print some statistics
print(f"Total rows: {results.total_rows}")
print(f"File size: {os.path.getsize(csv_filename) / (1024 * 1024):.2f} MB")
