import json
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
"""
Code from Jonathan Meier. "How to Query Google Drive API in Python".
_YouTube_, 13 June 2020, https://youtu.be/10ANOSssdCw.
"""

# If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/drive.metadata.readonly",
    "https://www.googleapis.com/auth/drive"
]


def get_credentials_as_dict(credentials) -> dict:
    credentials_as_dict = {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "id_token": credentials.id_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }
    return credentials_as_dict


def credentials_from_dict(credentials_dict: dict) -> Credentials:
    """Return credential object from dict"""
    # Need to explicitly pass each argument to Credentials
    creds = Credentials(
        credentials_dict["token"],
        refresh_token=credentials_dict["refresh_token"],
        token_uri=credentials_dict["token_uri"],
        client_id=credentials_dict["client_id"],
        client_secret=credentials_dict["client_secret"],
        scopes=credentials_dict["scopes"],
    )
    return creds


def get_credentials() -> Credentials:
    """Retrieves credentials from local cache or by executing auth flow"""

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    creds = None
    token_filename = "token.json"

    if os.path.exists(token_filename):
        with open(token_filename, "r") as f:
            credentials_as_dict = json.load(f)
            creds = credentials_from_dict(credentials_as_dict)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for next run
        with open(token_filename, "w") as f:
            f.write(creds.to_json())

    return creds


def list_files(service: None, page_size: int = 10):
    """List files from the drive service"""
    # Call the Drive v3 API
    results = (
        service.files()
        .list(pageSize=page_size, fields="nextPageToken, files(id, name)")
        .execute()
    )
    items = results.get("files", [])

    if not items:
        print("No files found.")
    else:
        print("Files:")
        for item in items:
            print(f'{item["name"]} ({item["id"]}')


def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    credentials = get_credentials()
    drive_service = build("drive", "v3", credentials=credentials)
    list_files(service=drive_service)


if __name__ == '__main__':
    main()
