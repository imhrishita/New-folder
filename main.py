#!/usr/bin/env python3
"""
AI-Powered Investor Communication Workflow
"""

import os
from src.config import Config
from src.data_reader import get_sheet_data, get_pending_rows, update_row
from src.validator import validate_row
from src.compliance import classify_message
from src.scheduler import schedule_message, start_scheduler

Config.validate()

def process_row(sheet, row_index, row):
    # Normalize row keys to lowercase for validation
    normalized_row = {k.lower(): v for k, v in row.items()}
    
    # Validation
    valid, error = validate_row(normalized_row)
    if not valid:
        update_row(sheet, row_index, {'status': 'Invalid'})
        return

    # Compliance check
    classification = classify_message(normalized_row['message'])
    update_row(sheet, row_index, {'compliance_flag': classification})

    if classification == 'Approved':
        update_row(sheet, row_index, {'status': 'Scheduled'})
        schedule_message(normalized_row, row_index, sheet)
    else:
        update_row(sheet, row_index, {'status': 'Blocked'})

def main():
    data, sheet = get_sheet_data()
    pending = get_pending_rows(data)

    for row_index, row in pending:
        process_row(sheet, row_index, row)

    # Start scheduler to send messages
    start_scheduler()

if __name__ == "__main__":
    try:
        main()
    except PermissionError:
        pass
    except FileNotFoundError:
        pass
    except ValueError:
        pass
    except Exception:
        pass