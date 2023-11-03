# modules/reporter.py

import smtplib
from email.message import EmailMessage
from config.settings import EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD

def send_email(subject, body, to_emails, attachment_path=None):
    """Send an email with an optional attachment."""
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_HOST_USER
    msg['To'] = to_emails
    msg.set_content(body)

    # Attach a file if the path is provided
    if attachment_path:
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
    to_emails = ["user@example.com"]  # Replace with your email
    send_email(subject, body, to_emails)

def send_daily_report(chart_path):
    """Send the daily candlestick chart via email."""
    subject = "Daily Candlestick Chart"
    body = "Please find attached the daily candlestick chart."
    to_emails = ["user@example.com"]  # Replace with your email
    send_email(subject, body, to_emails, chart_path)
