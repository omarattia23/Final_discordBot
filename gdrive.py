from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from _log import _logger

def gdrive():
    # Set up Google Drive API authentication using a service account
        scope = ['https://www.googleapis.com/auth/drive']
        Excel_SCOPE = ['https://www.googleapis.com/auth/spreadsheets.readonly']
        scopes = scope + Excel_SCOPE
        credentials = ServiceAccountCredentials.from_json_keyfile_name("RAScloud.json", scopes)

        gauth = GoogleAuth()
        gauth.credentials = credentials
        return GoogleDrive(gauth)

if __name__ == "__main__":
    gdrive()