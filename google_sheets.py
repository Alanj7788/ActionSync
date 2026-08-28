import os

import gspread

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from config import SCOPES


def get_google_sheets_client():

    creds = None

    # Load existing token
    if os.path.exists("token.json"):

        creds = Credentials.from_authorized_user_file(
            "token.json",
            SCOPES
        )

    # Authenticate if needed
    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:

            creds.refresh(Request())

        else:

            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES
            )

            creds = flow.run_local_server(port=0)

        # Save authentication token
        with open("token.json", "w") as token:

            token.write(creds.to_json())

    return gspread.authorize(creds), creds


def save_tasks_to_google_sheets(meeting_title, tasks):

    client, creds = get_google_sheets_client()

    # Create spreadsheet
    spreadsheet = client.create(meeting_title)

    worksheet = spreadsheet.sheet1

    # Make spreadsheet shareable
    drive_service = build(
        "drive",
        "v3",
        credentials=creds
    )

    drive_service.permissions().create(
        fileId=spreadsheet.id,
        body={
            "type": "anyone",
            "role": "reader"
        }
    ).execute()

    # Add headers
    worksheet.append_row([
        "Task",
        "Owner",
        "Deadline",
        "Priority",
        "Follow-up",
        "Status"
    ])

    # Prepare all task rows
    rows = []

    for task in tasks:

        rows.append([
            task["Task"],
            task["Owner"],
            task["Deadline"],
            task["Priority"],
            task["Follow-up"],
            task["Status"]
        ])

    # Add all rows at once
    if rows:

        worksheet.append_rows(rows)

    return spreadsheet.url