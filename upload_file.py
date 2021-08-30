import pickle
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload
"""
Code from Abdou Rockikz. "How to Use Google Drive API in Python". _PythonCode_,
https://www.thepythoncode.com/article/using-google-drive--api-in-python,
Retrieved 30 August 2021.
"""
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly',
          'https://www.googleapis.com/auth/drive.file']


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
            result.append((file["id"],
                           file["name"],
                           file["mimeType"]
                           ))
        page_token = response.get('nextPageToken', None)
        if not page_token:
            # no more files
            break
    return result


def upload_files():
    """
    Get the folder id and upload the file
    """
    # authenticate account
    service = get_gdrive_service()

    filename = "bbc.zip"
    foldername = "tmp"

    # Get the folder id
    search_result = search(service, query=f"name='{foldername}'")
    folder_id = search_result[0][0]

    # upload a file text file
    # first, define file metadata, such as the name and the parent folder ID
    file_metadata = {
        "name": [filename],
        "parents": [folder_id]
    }
    # upload
    media = MediaFileUpload(filename, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media,
                                  fields='id').execute()
    print("File created, id:", file.get("id"))


if __name__ == '__main__':
    upload_files()
