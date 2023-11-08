# modules/reporter.py

import smtplib
from email.message import EmailMessage
from config.settings import EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_TO, DRIVE_FOLDER
from datetime import datetime
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os.path

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']


def get_drive_service():
    """Log in to Google Drive and create a service object."""
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('config/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('drive', 'v3', credentials=creds)


def upload_to_drive(file_path, folder_name= DRIVE_FOLDER):
    """Uploads a file to a Google Drive folder with the specified name."""
    service = get_drive_service()

    # First, find the folder ID by the folder name
    folder_id = None
    response = service.files().list(q=f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'",
                                    spaces='drive',
                                    fields='nextPageToken, files(id, name)').execute()
    for folder in response.get('files', []):
        # Assume the first folder is the one we want
        folder_id = folder.get('id')
        break

    if not folder_id:
        # Create folder if not found
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = service.files().create(body=file_metadata, fields='id').execute()
        folder_id = folder.get('id')

    # File metadata
    file_metadata = {'name': os.path.basename(file_path), 'parents': [folder_id]}
    media = MediaFileUpload(file_path, resumable=True)
    # Call the Drive v3 API
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    #print(f"File ID: {file.get('id')}")

def get_date_str():
    """Get the current date as a string."""
    return datetime.now().strftime("%Y-%m-%d")

def send_email(subject, body, to_emails, attachment_paths=None):
    """Send an email with multiple optional attachments."""
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_HOST_USER
    msg['To'] = to_emails
    msg.set_content(body)

    # Attach files if paths are provided
    if attachment_paths:
        for attachment_path in attachment_paths:
            with open(attachment_path, 'rb') as attachment:
                file_data = attachment.read()
                file_name = attachment.name
                msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

    # Connect to the email server and send the email
    with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT) as smtp:
        smtp.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        smtp.send_message(msg)

def report_error(error):
    """Report an error via email."""
    subject = "Error Notification"
    body = f"An error has occurred: {error}\nPlease check manually."
    to_emails = EMAIL_TO
    send_email(subject, body, to_emails)

def send_daily_report(attachment_paths):
    """Send the daily reports via email with multiple attachments."""
    date_str = get_date_str()
    subject = f"Daily Reports {date_str}"
    body = "Please find attached the daily reports."
    to_emails = EMAIL_TO  # Replace with your email
    send_email(subject, body, to_emails, attachment_paths)

def send_daily_report_with_drive_upload(attachment_paths):
    """upload them to Google Drive."""
    # Upload to Google Drive
    for attachment_path in attachment_paths:
        upload_to_drive(attachment_path)