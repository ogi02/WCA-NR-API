# Python dependencies
import os
import smtplib
from email.message import EmailMessage

# Project dependencies
from wca_nr_api.config.logger import logger_filename


def send_email(success: bool) -> None:
    """
    Sends email with the log file as an attachment to the list of recipients.

    :param success: (bool) Whether the API has succeeded.
    """

    # Email Configuration
    smtp_server = os.environ["SMTP_SERVER"]
    smtp_port = os.environ["SMTP_PORT"]
    sender_email = os.environ["SENDER_EMAIL"]
    sender_password = os.environ["SENDER_PASSWORD"]
    recipient_email = os.environ["RECIPIENT_EMAIL"]

    # Create email message
    msg = EmailMessage()
    msg["Subject"] = f"WCA NR API Execution - {'Success' if success else 'Failure'}"
    msg["From"] = sender_email
    msg["To"] = recipient_email

    # Attach file
    if not os.path.exists(logger_filename):
        raise FileNotFoundError(f"Attachment not found: {logger_filename}")

    with open(logger_filename, "rb") as f:
        file_data = f.read()
        file_name = os.path.basename(logger_filename)
        msg.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file_name)

    # Send email
    with smtplib.SMTP(smtp_server, int(smtp_port)) as server:
        # Secure the connection
        server.starttls()
        try:
            # Login and send message
            server.login(sender_email, sender_password)
            server.send_message(msg)
        except Exception as e:
            raise e
