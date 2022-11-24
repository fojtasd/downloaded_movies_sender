from __future__ import print_function
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from apiclient import discovery
from google.oauth2 import service_account

import os
import os.path
import glob
import httplib2

list_movies = []
list_series = []
sorted_list_movies = [[]]
sorted_list_series = [[]]
path0 = glob.glob('/home/davidf/HDD/movies/**/*', recursive=True)
path1 = glob.glob('/home/davidf/HDD1/**/*', recursive=True)
path2 = glob.glob('/home/davidf/HDD2/movies/**/*', recursive=True)
path_series = glob.glob('/home/davidf/HDD2/series/**/*', recursive=True)

def movies_getter(path):
    for f in path:
        p = Path(f)
        if p.suffix in [".mkv", ".avi", ".mp4", ".mpeg4"]:
            list_movies.append([p.name])

def series_getter(path):
    for f in path:
        p = Path(f)
        if p.suffix in [".mkv", ".avi", ".mp4", ".mpeg4"]:
            list_series.append([p.name])

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
spreadsheet_id = '1mQslDdUiIiKM9u4Uib9IpxNuNSanQgQEJ7x5cqc81yE'
range_name_movies = 'movies!A:A'
range_name_series = 'series!A:A'

def main():
    movies_getter(path0)
    movies_getter(path1)
    movies_getter(path2)
    names = [a[0] for a in list_movies]
    names.sort()
    sorted_list_movies = [[a] for a in names]

    series_getter(path_series)
    names = [a[0] for a in list_series]
    names.sort()
    sorted_list_series = [[a] for a in names]


    #tady jsem skončil zatim
    subdirectories = glob.glob("/home/davidf/HDD2/series/*/")
    names = [os.path.basename(x) for x in glob.glob("/home/davidf/HDD2/series/*/")]
    print(names)

    try:
        secret_file = os.path.join(os.getcwd(), 'client_secret.json')
        credentials = service_account.Credentials.from_service_account_file(secret_file, scopes=SCOPES)
        service = discovery.build('sheets', 'v4', credentials=credentials)
        resource_movies = {
            "majorDimension": "ROWS",
            "values": sorted_list_movies
        }
        resource_series = {
            "majorDimension": "ROWS",
            "values": list_series
        }
        service = build('sheets', 'v4', credentials=credentials)
        service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=range_name_movies, body=resource_movies, valueInputOption="USER_ENTERED").execute()
        service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=range_name_series, body=resource_series, valueInputOption="USER_ENTERED").execute()
    except HttpError as err:
        print(err)

if __name__ == '__main__':
    main()