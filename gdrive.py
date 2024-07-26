from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from utils import decrypt
import json, os
from dotenv import load_dotenv
def gdrive():
    # Set up Google Drive API authentication using a service account
    key = os.getenv('KEY')

    if not key:
        raise ValueError("KEY not found in environment variables")

    
    key = key.encode()
    secret = decrypt(key)
    secret = json.loads(secret)

    scope = ['https://www.googleapis.com/auth/drive']
    Excel_SCOPE = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    scopes = scope + Excel_SCOPE
    
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(secret, scopes)

    gauth = GoogleAuth()
    gauth.credentials = credentials
 
    return GoogleDrive(gauth)

if __name__ == "__main__":
    gdrive()
    


