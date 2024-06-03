import base64, re, datetime
from pathlib import Path
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from domain.consts import SystemConstants
from lib.config import load_config
from src.google_auth import get_cledential
from src.filename_formatter import filename_format

config = load_config(SystemConstants.config)
SCOPES = [config["gmail"]["url_readonly"]]
SAVE_AS_DIR_PATH = Path(config["gmail"]["save_dir"])
pattern = config["gmail"]["zipfile_pattern"]

# decode data which is encoded by Base64URL
def decode_base64url(data):
    if data:
        return base64.urlsafe_b64decode(data.encode(SystemConstants.encode))
    return None

def search_emails(service, query):
    results = service.users().messages().list(userId='me', q=query).execute()
    messages = results.get('messages', [])
    return messages

def get_email_details(service, msg_id):
    message = service.users().messages().get(userId='me', id=msg_id).execute()
    return message

# A function to download and save attachments
def download_attachment(service, userId, msg_Id, attachment_id, filepath):
    attachment = (
        service.users()
        .messages()
        .attachments()
        .get(userId=userId, messageId=msg_Id, id=attachment_id)
        .execute()
    )
    file_data = decode_base64url(attachment["data"])
    with open(filepath, "wb") as f:
        f.write(file_data)
    print(f"Saved attachment to {str(filepath)}")

# A function to search for and download attachments from a message
def find_and_download_attachments(service, query: str, userId: str, directory: Path):
    directory.mkdir(exist_ok=True)
    messages = search_emails(service=service, query=query)
    print(messages)

    i = 0
    for msg in messages:
        msg_id = msg["id"]
        message = get_email_details(service, msg_id)

        for part in message["payload"].get("parts", []):
            filename = filename_format(part.get("filename"))
            print(filename)
            if filename and re.match(pattern, filename):
                body = part.get("body", {})
                attachment_id = body.get("attachmentId")
                print(filename)
                if attachment_id:
                    # If an attachment is found, download it
                    print(f"filename: {filename}, attachment_id: {attachment_id}")
                    filepath = directory / filename
                    download_attachment(service, userId, msg_id, attachment_id, filepath)
                    i += 1
                if "parts" in part:
                    # If nested, search recursively
                    find_and_download_attachments(service, msg_id, part, userId, directory)
    print(f"{i} mails found")

def job():
    creds = get_cledential(SCOPES)

    subject = config["gmail"]["subject"]
    # Set the time range from the current time to 10 minutes ago
    now = datetime.datetime.now()
    ten_minutes_ago = now - datetime.timedelta(minutes=10)
    now_timestamp = int(now.timestamp())
    ten_minutes_ago_timestamp = int(ten_minutes_ago.timestamp())
    query = f"subject:{subject} after:{ten_minutes_ago_timestamp} before:{now_timestamp}"

    try:
        service = build("gmail", "v1", credentials=creds)
        find_and_download_attachments(
            service, query, "me", SAVE_AS_DIR_PATH
        )
    except HttpError as error:
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    job()