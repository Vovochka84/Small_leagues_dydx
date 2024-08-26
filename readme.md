# DYDX Transaction Analysis

This project analyzes DYDX transactions for ranked recipients across different seasons.

## Features

- Processes transaction data for silver and bronze tier recipients
- Generates reports for each season and tier
- Filters transactions based on date ranges for each season
- Identifies senders with multiple ranked recipients
- Identifies ranked senders who sent money to multiple recipients

## Usage

1. Place your transaction data in a file named `transfer_txs.csv` in the project root.
2. Place your ranked recipient files (e.g., `silver_s2.csv`, `bronze_s2.csv`) in the `Leaderboards` directory.
3. Run the script:

   ```
   python main.py
   ```

4. Reports will be generated in the project root as `report_silver_s2.txt`, `report_bronze_s2.txt`, etc.

## File Structure

- `main.py`: The main script that processes the data and generates reports
- `transfer_txs.csv`: Contains all transaction data
- `Leaderboards/`: Directory containing ranked recipient files for each season and tier
- `report_*.txt`: Generated reports (not tracked in Git)

## Requirements

- Python 3.6+
- CSV files with the correct structure for transactions and ranked recipients
