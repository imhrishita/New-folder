# AI-Powered Investor Communication Workflow

This project builds an AI-powered workflow that reads scheduled investor communication data from a Google Sheet, validates inputs, applies a compliance guardrail layer before sending, and sends approved messages at scheduled times.

## Features

- Reads data from Google Sheets
- Validates input data
- Applies compliance checks using LLM
- Schedules and sends messages via SMS or email

## Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Configure Google Sheets API credentials
3. Set up LLM API (e.g., OpenAI)
4. Configure messaging service (e.g., Twilio for SMS)

## Usage

Run the main script: `python main.py`