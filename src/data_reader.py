"""
Data reading layer
"""

import gspread
from google.oauth2 import service_account
from src.config import Config

def get_sheet_client():
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = service_account.Credentials.from_service_account_file(Config.GOOGLE_CREDENTIALS_PATH, scopes=scopes)
    client = gspread.authorize(creds)
    return client

def get_sheet_data():
    client = get_sheet_client()
    sheet = client.open_by_key(Config.GOOGLE_SHEET_ID).sheet1
    data = sheet.get_all_records()
    return data, sheet

def get_pending_rows(data):
    pending = []
    for i, row in enumerate(data, start=2):  # Assuming header is row 1
        if not row.get('status') or row.get('status') == 'Pending':
            pending.append((i, row))
    return pending

def update_row(sheet, row_index, updates):
    for col, value in updates.items():
        col_index = get_column_index(col)
        sheet.update_cell(row_index, col_index, value)

def get_column_index(col_name):
    columns = ['name', 'mobile', 'message', 'schedule', 'category', 'status', 'compliance_flag']
    return columns.index(col_name.lower()) + 1