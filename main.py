#!/usr/bin/env python3
"""
AI-Powered Investor Communication Workflow
"""

import os
from dotenv import load_dotenv
from src.data_reader import get_sheet_data, get_pending_rows, update_row
from src.validator import validate_row
from src.compliance import classify_message
from src.scheduler import schedule_message, start_scheduler

load_dotenv()

def process_row(sheet, row_index, row):
    # Validation
    valid, error = validate_row(row)
    if not valid:
        update_row(sheet, row_index, {'status': 'Invalid'})
        print(f"Row {row_index}: Invalid - {error}")
        return

    # Compliance check
    classification = classify_message(row['message'])
    update_row(sheet, row_index, {'compliance_flag': classification})

    if classification == 'Approved':
        update_row(sheet, row_index, {'status': 'Scheduled'})
        schedule_message(row, row_index, sheet)
        print(f"Row {row_index}: Scheduled")
    else:
        update_row(sheet, row_index, {'status': 'Blocked'})
        print(f"Row {row_index}: Blocked - {classification}")

def main():
    print("Starting AI-powered investor communication workflow...")
    data, sheet = get_sheet_data()
    pending = get_pending_rows(data)

    for row_index, row in pending:
        process_row(sheet, row_index, row)

    # Start scheduler to send messages
    start_scheduler()

if __name__ == "__main__":
    main()