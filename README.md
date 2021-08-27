# Google Drive API v3: Python Quickstart
Material taken from Quickstart for the Google Drive API v3:

"Google Drive for Developers v3: Python Quickstart". _Google Developers_,
https://developers.google.com/drive/api/v3/quickstart/python, retrieved 27
August 2021.

Original contents licensed by Google under Creating Commons Attribution
4.0 license and code samples under the Apache 2.0 license.

## Procedure

1. Sign into the Google Cloud Console.
2. Create a new project.
3. Enable the Google Drive API for the project.
4. Configure the OAuth consent screen.
5. Generate credentials.
6. Run script.

## Notes

### OAuth consent screen configuration

_User Type_. If using a personal Google account rather than a Google Workspace (GSuite) account, the app must be configured as External. The Google Developer tutorial assumes that you are using a Google Workspace account, and so proceeds to configure for an Internal app.

_App Information_. Provide the name of the app and your e-mail for "User support email".

_App Domain_. Leave blank unless you are using a Google Workspace account.

_Developer Contact Information_. Provide your e-mail.

_Scopes_. Add the following scopes:
    * Google Drive API /auth/drive.metadata.readonly
    * Google Drive API /auth/drive

_Test Users_. Add your account as a test user.

### Credentials

_Applicatiom type_. Desktop app.

_Name_. Whatever sounds good to you.

After generating the credentials, click on the download icon all the way to the right and save as "credentials.json" in the project folder on your computer. This file should be kept secret from the world, so if your files are being tracked by git be sure to add "credentials.json" and "token.json" (the latter will be created by the script and will contain a copy of these credentials) to the .gitignore file for the project.

### Additional Resources

In his tutorial on the Google Drive API, Jonathan Meier configures for a personal Google account. Jonathan Meier. "How to Query Google Drive API in Python". _YouTube_, 13 June 2020, https://youtu.be/10ANOSssdCw. I have also included his script here (renamed to "listfiles.py") because it demonstrates an alternative pattern for structuring the code. In his 11 minute video, which I highly recommend, Jonathan does a terrific job of explaining the how this all works.
