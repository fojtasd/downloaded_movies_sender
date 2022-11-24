import os
import os.path
import glob
from pathlib import Path
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

spreadsheet_id = '1mQslDdUiIiKM9u4Uib9IpxNuNSanQgQEJ7x5cqc81yE'
range_name_movies = 'movies!A:A'
range_name_series = 'series!A:A'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

list_media = []
list_folders = []
sorted_list_media = [[]]

path0 = glob.glob('/home/davidf/HDD/movies/**/*', recursive=True)
path1 = glob.glob('/home/davidf/HDD1/**/*', recursive=True)
path2 = glob.glob('/home/davidf/HDD2/movies/**/*', recursive=True)
path_series = glob.glob('/home/davidf/HDD2/series/*')


def media_getter(path):
    for f in path:
        p = Path(f)
        if p.suffix in [".mkv", ".avi", ".mp4", ".mpeg4"]:
            list_media.append([p.name])


def series_getter(path):
    for f in path:
        p = Path(f)
        path_temp = glob.glob('/home/davidf/HDD2/series/' + p.name + '/*')
        list_media.append(["######################################"])
        list_media.append([p.name])

        for f in path_temp:
            p = Path(f)
            if p.suffix in [".mkv", ".avi", ".mp4", ".mpeg4"]:
                list_media.append([p.name])


def list_sorter(list_to_sort):
    names = [a[0] for a in list_to_sort]
    names.sort()
    sorted_list_media = [[a] for a in names]
    return sorted_list_media


def main():
    try:
        secret_file = os.path.join(os.getcwd(), 'client_secret.json')
        credentials = service_account.Credentials.from_service_account_file(secret_file, scopes=SCOPES)
        service = build('sheets', 'v4', credentials=credentials)

        # series_getter
        series_getter(path_series)
        resource_series = {
            "majorDimension": "ROWS",
            "values": list_media
        }

        service.spreadsheets().values().clear(spreadsheetId=spreadsheet_id, range=range_name_series).execute()
        service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=range_name_series,
                                               body=resource_series, valueInputOption="USER_ENTERED").execute()

        # movies getter
        list_media.clear()
        media_getter(path0)
        media_getter(path1)
        media_getter(path2)
        sorted_list_media = list_sorter(list_media)

        resource_movies = {
            "majorDimension": "ROWS",
            "values": sorted_list_media
        }
        service.spreadsheets().values().clear(spreadsheetId=spreadsheet_id, range=range_name_movies).execute()
        service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=range_name_movies,
                                               body=resource_movies, valueInputOption="USER_ENTERED").execute()
    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()
