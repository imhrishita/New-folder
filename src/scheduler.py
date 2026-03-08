"""
Scheduling layer
"""

from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
from src.sender import send_message

scheduler = BlockingScheduler()

def schedule_message(row, row_index, sheet):
    dt = datetime.strptime(row['schedule'], '%Y-%m-%d %H:%M')
    scheduler.add_job(send_message, 'date', run_date=dt, args=[row, row_index, sheet])

def start_scheduler():
    scheduler.start()