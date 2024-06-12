# google_auth.py
import os
from pathlib import Path
from domain.consts import SystemConstants
from lib.config import load_config
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
config = load_config(SystemConstants.config)
from src.mail.mail import EmailController

# Where to store tokens and credentials
cred_json = Path(config["googleapi"]["client_secret"])
token_save_path_gmail = Path(config["gmail"]["token"])
token_save_path_drive = Path(config["drive"]["token"])

def mail_sender(output=""):
    with open(config["mail"]["template"], 'r', encoding=SystemConstants.encode) as f:
        body = f.read()
    notice_mail = EmailController(config["mail"]["from"], config["mail"]["host"], config["mail"]["port"], config["mail"]["password"])
    body += output
    notice_mail.create(config["mail"]["to"], config["mail"]["subject"], body)
    notice_mail.send()

# Functions for obtaining credentials
def get_cledential(scopes: list[str]) -> Credentials:
    """
    Obtains Google API authentication information using the OAuth2 authentication flow (client secret).
    Returns authentication information if it already exists.
    Supports refresh tokens.
    If not, obtains authentication information and saves it in google_api_access_token.json.
    args:
    scopes: Scopes required to obtain authentication information
    return:
    Authentication information
    """
    if "gmail" in scopes[0]:
        token_save_path = token_save_path_gmail
    elif "drive" in scopes[0]:
        token_save_path = token_save_path_drive
    else:
        print("Error on getting token_save_path")
        return None
    
    creds = None
    if token_save_path.exists():
        creds = Credentials.from_authorized_user_file(token_save_path, scopes)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception:
                os.remove(config["googleapi"]["token"])
                mail_sender()
                get_cledential(scopes)
        else:
            flow = InstalledAppFlow.from_client_secrets_file(cred_json, scopes)
            creds = flow.run_local_server(port=0)
        with token_save_path.open("w") as token:
            token.write(creds.to_json())
    return creds