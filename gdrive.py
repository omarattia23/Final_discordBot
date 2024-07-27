from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from utils import decrypt
import json, os
from dotenv import load_dotenv
from io import BytesIO
def gdrive():
    load_dotenv('.env')
    # Set up Google Drive API authentication using a service account
    key = os.getenv('KEY01')
    if not key:
        raise ValueError("KEY not found in environment variables")

    key = key.encode()
    secret = decrypt(key)
    try:
        secret = json.loads(secret)
    except json.JSONDecodeError:
        raise ValueError("Failed to parse decrypted secret as JSON")


    scope = ['https://www.googleapis.com/auth/drive']
    Excel_SCOPE = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    scopes = scope + Excel_SCOPE
    
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(secret, scopes)

    gauth = GoogleAuth()
    gauth.credentials = credentials

    print("Successfully authenticated with Google Drive API")
    return GoogleDrive(gauth)

if __name__ == "__main__":
    pass
    
