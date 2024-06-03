# google_auth.py
from domain.consts import SystemConstants
from lib.config import load_config
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
config = load_config(SystemConstants.config)

# Where to store tokens and credentials
token_save_path = config["googleapi"]["token"]
cred_json = config["googleapi"]["client_secret"]

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
    creds = None
    if token_save_path.exists():
        creds = Credentials.from_authorized_user_file(token_save_path, scopes)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(cred_json, scopes)
            creds = flow.run_local_server(port=0)
        with token_save_path.open("w") as token:
            token.write(creds.to_json())
    return creds