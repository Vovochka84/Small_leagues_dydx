# DYDX Transaction Analysis

This project analyzes DYDX transactions for ranked recipients across different seasons.

## Features

- Processes transaction data for silver and bronze tier recipients
- Generates reports for each season and tier
- Filters transactions based on date ranges for each season
- Identifies senders with multiple ranked recipients
- Identifies ranked senders who sent money to multiple recipients

## Usage

1. The transaction data file `transfer_txs.csv` is included in the root of the repository.
2. Place your ranked recipient files (e.g., `silver_s2.csv`, `bronze_s2.csv`) in the `Leaderboards` directory.
3. Run the script:

   ```
   python main.py
   ```

4. Reports will be generated in the project root as `report_silver_s2.txt`, `report_bronze_s2.txt`, etc.

## File Structure

- `main.py`: The main script that processes the data and generates reports
- `transfer_txs.csv`: Contains all transaction data
- `Leaderboards/`: Directory containing ranked recipient files for each season and tier (not tracked in Git)
- `report_*.txt`: Generated reports (not tracked in Git)

## Report Structure

Each report (`report_{tier}_{season}.txt`) contains:

1. Header: Report title and date range
2. Summary statistics: Total ranked recipients, transactions processed, and matching transactions
3. Matching transactions:
   - Recipient address and rank
   - For each sender:
     - Sender address
     - Total USDC amount
     - Number of transactions
     - Up to 5 transaction hashes
4. Senders with multiple ranked recipients
5. Ranked senders who sent to multiple recipients

Key points:

- Transactions are filtered by date range for each season
- Only transactions to ranked recipients are included
- Recipients are sorted by rank, senders by total USDC amount
- USDC amounts are displayed with 2 decimal places

## Generating Transaction Data

The project includes a script to generate the `transfer_txs.csv` file by querying the BigQuery database:

- `generate_transfer_txs.py`: This script queries the BigQuery database to generate the `transfer_txs.csv` file.

To use this script:

1. Ensure you have the `google-cloud-bigquery` library installed:

   ```
   pip install google-cloud-bigquery
   ```

2. Place your `credentials.json` file (containing your Google Cloud service account key) in the project root.

3. Run the script:

   ```
   python generate_transfer_txs.py
   ```

This will generate the `transfer_txs.csv` file in the project root, containing withdrawal transactions where the sender and recipient are different.

Note: Running this script may incur costs in your Google Cloud account due to BigQuery usage. Be mindful of potential charges when running queries on large datasets.

## Requirements

- Python 3.6+
- CSV files with the correct structure for transactions and ranked recipients

## Note

The `transfer_txs.csv` file is included in this repository for convenience. Be cautious about committing updates to this file if it contains sensitive information.
