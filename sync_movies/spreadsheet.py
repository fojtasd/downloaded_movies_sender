import os
import os.path
from typing import List, Any

from google.oauth2 import service_account
from googleapiclient.discovery import build


spreadsheet_id = '1mQslDdUiIiKM9u4Uib9IpxNuNSanQgQEJ7x5cqc81yE'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def get_spreadsheet() -> Any:
    secret_file = os.path.join(os.getcwd(), 'client_secret.json')
    credentials = service_account.Credentials.from_service_account_file(secret_file, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials)

    return service.spreadsheets()

def write_to_spreadsheet(sheet: Any, sheet_range: str, data: List[List[str]]) -> None:
    sheet.values().clear(spreadsheetId=spreadsheet_id, range=sheet_range).execute()
    sheet.values().update(
        spreadsheetId=spreadsheet_id, 
        range=sheet_range, 
        body={
            "majorDimension": "ROWS",
            "values": data
        }, 
        valueInputOption="USER_ENTERED"
    ).execute()
