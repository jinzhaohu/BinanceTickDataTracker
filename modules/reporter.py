# modules/reporter.py

import smtplib
from email.message import EmailMessage
from config.settings import EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_TO
from datetime import datetime

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