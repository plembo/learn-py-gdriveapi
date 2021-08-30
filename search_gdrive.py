
import pickle
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from tabulate import tabulate
"""
Code from Abdou Rockikz. "How to Use Google Drive API in Python". _PythonCode_,
https://www.thepythoncode.com/article/using-google-drive--api-in-python,
Retrieved 30 August 2021.
"""

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata']


def get_gdrive_service():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('drive', 'v3', credentials=creds)


def search(service, query):
    # search for the file
    result = []
    page_token = None
    while True:
        response = service.files().list(
            q=query,
            spaces="drive",
            fields="nextPageToken, files(id, name, mimeType, size)",
            pageToken=page_token).execute()
        # iterate over filtered files
        for file in response.get("files", []):
            file_size = get_size_format(int(file["size"]))
            result.append((file["id"],
                           file["name"],
                           file["mimeType"],
                           file_size))
        page_token = response.get('nextPageToken', None)
        if not page_token:
            # no more files
            break
    return result


def get_size_format(b, factor=1024, suffix="B"):
    """
    Scale bytes to its proper byte format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"


def main():
    # filter to file name
    filename = 'opendj'
    # authenticate Google Drive API
    service = get_gdrive_service()
    # search for files that has type of text/plain
    search_result = search(service, query=f"name contains '{filename}'")
    # convert to table to print well
    table = tabulate(search_result, headers=["ID", "Name", "Type", "Size"])
    print(table)


if __name__ == '__main__':
    main()
