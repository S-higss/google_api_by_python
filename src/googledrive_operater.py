import mimetypes
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
# import libs
from lib.config import load_config
from domain.consts import SystemConstants
from src.google_auth import get_cledential

# load config
config = load_config(SystemConstants.config)

# If modifying these scopes, delete the file token.pickle.
SCOPES = [config["drive"]["url"]]

class Drive:
    def __init__(self):
        # load config
        self.config = load_config(SystemConstants.config)
        creds = get_cledential(SCOPES)
        try:
            # create drive api client
            self.service = build('drive', 'v3', credentials=creds)
        except HttpError as error:
            # TODO(developer) - Handle errors from drive API.
            print(f'An error occurred: {error}')
            self.service = None

    def create_folder(self, folder_name):
        """ Creates a folder and prints the folder ID
        Returns : Folder Id
        """
        try:
            # create drive api client
            file_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            # pylint: disable=maybe-no-member
            file = self.service.files().create(
                body=file_metadata, 
                fields='id'
            ).execute()
            print(F'Folder ID: "{file.get("id")}".')
            return file.get('id')

        except HttpError as error:
            print(F'An error occurred: {error}')
            return None

    def upload(self, file_name, file_path, folder_id):
        """ Uploads a file and prints the file ID
        Returns : File Id
        """
        try:
            # metadata(for Google Drive): file name and destination folder id
            file_metadata = {
                'name': file_name,
                'parents': [folder_id]
            }
            # media_data(for handling file): file path and file extension, resumable upload or not
            media = MediaFileUpload(
                file_path,
                mimetype=mimetypes.guess_type(file_path)[0],
                resumable=True
            )
            file = self.service.files().create(
                body=file_metadata, media_body=media, fields='id'
            ).execute()
            file_id = file.get('id')
            print('File ID: %s' % file_id)
        except HttpError as error:
            # TODO(developer) - Handle errors from drive API.
            print(f'An error occurred: {error}')
            file_id = None
        return file_id
    
    def delete(self, file_id):
        """ Deletes a file
        Returns : None
        """
        try:
            self.service.files().delete(fileId=file_id).execute()
        except HttpError as error:
            # TODO(developer) - Handle errors from drive API.
            print(f'An error occurred: {error}')
    
    def list(self):
        """ Prints files in Google Drive
        Returns : None
        """
        try:
            results = self.service.files().list(
                pageSize=10, fields="nextPageToken, files(id, name)").execute()
            items = results.get('files', [])
            if not items:
                print('No files found.')
                return
            print('Files in Google Drive:')
            for item in items:
                print(u'{0} ({1})'.format(item['name'], item['id']))
        except HttpError as error:
            # TODO(developer) - Handle errors from drive API.
            print(f'An error occurred: {error}')

def main():
    config = load_config(SystemConstants.config)
    drive = Drive()
    mode = ""

    while mode != 0:
        mode = input(
            "Input the number you want to do by using Drive API.\n"
            + "1: Get files list\n"
            + "2: Create folder\n"
            + "3: Upload files\n"
            + "4: Delete files\n"
            + "0: Exit\n"
            + "Enter: "
        )
        mode = int(mode)
        if mode == 1:
            print("These are files list in google drive.")
            drive.list()
        elif mode == 2:
            name = input("enter folder name: ")
            drive.create_folder(name)
        elif mode == 3:
            drive.upload("crawling.log", config["log"]["crawling"], config["drive"]["folder_id_test"])
        elif mode == 4:
            id = input("enter folder id you wanna delete: ")
            drive.delete(id)
        else: pass

if __name__ == '__main__':
    main()