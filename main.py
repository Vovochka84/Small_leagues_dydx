import csv
import os
from collections import defaultdict
from datetime import datetime, date


def read_recipients(ranked_file):
    recipients = {}
    with open(ranked_file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            recipients[row["account"]] = row["rank"]
    return recipients


def get_date_range(filename):
    if "s2" in filename.lower():
        return date(2024, 1, 4), date(2024, 2, 22)
    elif "s3" in filename.lower():
        return date(2024, 2, 23), date(2024, 4, 10)
    elif "s4" in filename.lower():
        return date(2024, 4, 11), date(2024, 5, 28)
    elif "s5" in filename.lower():
        return date(2024, 5, 29), date(2024, 7, 17)
    elif "s6" in filename.lower():
        return date(2024, 7, 16), None  # No end date for s6
    else:
        return None, None  # No date filtering for other files


def process_transactions(transactions_file, ranked_recipients, start_date, end_date):
    matching_transactions = defaultdict(lambda: defaultdict(list))
    sender_to_recipients = defaultdict(set)
    total_transactions = 0
    matching_count = 0

    with open(transactions_file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            total_transactions += 1
            tx_date = datetime.strptime(
                row["block_timestamp"].split()[0], "%Y-%m-%d"
            ).date()

            if start_date and tx_date < start_date:
                continue
            if end_date and tx_date > end_date:
                continue

            recipient = row.get("recipient", "").strip()
            sender = row.get("sender", "").strip()
            if recipient in ranked_recipients:
                matching_transactions[recipient][sender].append(row)
                sender_to_recipients[sender].add(recipient)
                matching_count += 1

    return (
        matching_transactions,
        sender_to_recipients,
        total_transactions,
        matching_count,
    )


def generate_report(ranked_file, transactions_file):
    ranked_recipients = read_recipients(ranked_file)
    start_date, end_date = get_date_range(os.path.basename(ranked_file))
    matching_transactions, sender_to_recipients, total_transactions, matching_count = (
        process_transactions(transactions_file, ranked_recipients, start_date, end_date)
    )

    report_name = f"report_{os.path.basename(ranked_file).rsplit('.', 1)[0]}.txt"

    with open(report_name, "w") as report:
        report.write(f"Report for {os.path.basename(ranked_file)}\n\n")
        if start_date:
            report.write(
                f"Date range: {start_date} to {end_date if end_date else 'end'}\n\n"
            )
        report.write(f"Total ranked recipients: {len(ranked_recipients)}\n")
        report.write(f"Total transactions processed: {total_transactions}\n")
        report.write(f"Matching transactions found: {matching_count}\n\n")

        if matching_transactions:
            report.write("Matching transactions:\n")
            for recipient, senders in matching_transactions.items():
                rank = ranked_recipients[recipient]
                report.write(f"\nRecipient: {recipient} (Rank: {rank})\n")
                for sender, transactions in senders.items():
                    total_amount = sum(float(tx.get("USDC", 0)) for tx in transactions)
                    report.write(f"  Sender: {sender}\n")
                    report.write(f"  Total USDC Amount: {total_amount:.2f}\n")
                    report.write(f"  Number of transactions: {len(transactions)}\n")
                    report.write("  Transaction Hashes:\n")
                    for tx in transactions[:5]:  # Limit to first 5 transaction hashes
                        report.write(f"    - {tx.get('tx_hash', 'N/A')}\n")
                    if len(transactions) > 5:
                        report.write(
                            f"    ... and {len(transactions) - 5} more transactions\n"
                        )
                    report.write("  ---\n")
        else:
            report.write("No matching transactions found.\n")

        report.write("\nSenders with multiple ranked recipients:\n")
        for sender, recipients in sender_to_recipients.items():
            if len(recipients) > 1:
                report.write(f"\nSender: {sender}\n")
                report.write("Recipients (Rank):\n")
                for recipient in recipients:
                    report.write(f"  - {recipient} ({ranked_recipients[recipient]})\n")

        report.write("\nRanked senders who sent money to multiple recipients:\n")
        for sender, recipients in sender_to_recipients.items():
            if sender in ranked_recipients and len(recipients) > 1:
                report.write(
                    f"\nSender: {sender} (Rank: {ranked_recipients[sender]})\n"
                )
                report.write("Recipients (Rank):\n")
                for recipient in recipients:
                    report.write(f"  - {recipient} ({ranked_recipients[recipient]})\n")

    print(f"Report generated: {report_name}")


def main():
    transactions_file = "transfer_txs.csv"
    ranked_lists_dir = ""

    try:
        seasons = ["s2", "s3", "s4", "s5", "s6"]
        tiers = ["silver", "bronze"]
        for season in seasons:
            for tier in tiers:
                ranked_file = os.path.join(ranked_lists_dir, f"{tier}_{season}.csv")
                if os.path.exists(ranked_file):
                    generate_report(ranked_file, transactions_file)

    except FileNotFoundError as e:
        print(f"Error: File not found - {e.filename}")
    except csv.Error as e:
        print(f"Error reading CSV file: {e}")


if __name__ == "__main__":
    main()
