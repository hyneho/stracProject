import os
from abc import ABC, abstractmethod
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload


# Base class for all storage operations
class StorageOperation(ABC):
    def __init__(self, credentials):
        print("Initializing Google Drive client...")
        self.service = build('drive', 'v3', credentials=credentials)

    @abstractmethod
    def execute(self):
        pass


# Helper function to get folder ID by folder name
def get_folder_id_by_name(service, folder_name):
    query = f"mimeType = 'application/vnd.google-apps.folder' and name = '{folder_name}' and 'root' in parents"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        return None  # Folder doesn't exist
    else:
        return items[0]['id']  # Return the ID of the first folder found

def list_and_choose_file(service):
    # List files in Google Drive root directory
    results = service.files().list(q="'root' in parents", fields="files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print("No files found in Google Drive.")
        return None

    # List the files and ask the user to select one
    print("Select a file by number:")
    for idx, item in enumerate(items):
        print(f"{idx + 1}. {item['name']}")

    try:
        choice = int(input("Enter the number of the file: "))
        if choice < 1 or choice > len(items):
            print("Invalid choice.")
            return None
        selected_file = items[choice - 1]
        return selected_file  # Return the selected file
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return None

# Upload operation
class UploadOperation(StorageOperation):
    def __init__(self, credentials, source, folder_name=None):
        super().__init__(credentials)
        self.source = source
        self.folder_name = folder_name

    def execute(self):
        # Check if the path is relative or absolute
        if not os.path.isabs(self.source):
            # If it's a relative path, convert it to absolute path based on the current directory
            self.source = os.path.abspath(self.source)

        # Ensure the file exists at the given path
        if not os.path.exists(self.source):
            print(f"Error: The file {self.source} does not exist.")
            return

        # Get the file name from the local path
        file_name = os.path.basename(self.source)

        # If a folder name is provided, get the folder ID
        folder_id = None
        if self.folder_name:
            folder_id = get_folder_id_by_name(self.service, self.folder_name)

            # If folder doesn't exist, create it
            if not folder_id:
                print(f"Folder '{self.folder_name}' not found. Creating folder...")
                folder_metadata = {
                    'name': self.folder_name,
                    'mimeType': 'application/vnd.google-apps.folder'
                }
                folder = self.service.files().create(body=folder_metadata, fields='id').execute()
                folder_id = folder.get('id')
                print(f"Created folder '{self.folder_name}' with ID: {folder_id}")

        # Prepare metadata for the upload
        file_metadata = {'name': file_name}
        if folder_id:
            file_metadata['parents'] = [folder_id]

        # Upload the file
        media = MediaFileUpload(self.source, resumable=True)
        uploaded_file = self.service.files().create(
            body=file_metadata, media_body=media, fields='id'
        ).execute()

        print(f"Uploaded {self.source} with file ID: {uploaded_file.get('id')}")


class DownloadOperation(StorageOperation):
    def __init__(self, credentials, file_name=None, destination_folder='.'):
        super().__init__(credentials)
        self.file_name = file_name
        self.destination_folder = destination_folder

    def execute(self):
        if self.file_name:
            # Directly download the file if filename is provided
            self.download_file_by_name(self.file_name)
        else:
            # If no filename provided, list the files and prompt the user to select one
            self.list_and_choose_file_for_download()

    def download_file_by_name(self, file_name):
        # Search for the file by its name
        query = f"name='{file_name}'"
        results = self.service.files().list(q=query, fields="files(id, name)").execute()
        files = results.get('files', [])

        if not files:
            print(f"No file found with the name '{file_name}'.")
            return

        file_id = files[0]['id']
        print(f"Found file: {file_name} (ID: {file_id})")

        # Download the file
        request = self.service.files().get_media(fileId=file_id)
        with open(f"{self.destination_folder}/{file_name}", 'wb') as f:
            downloader = MediaIoBaseDownload(f, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
                print(f"Download progress: {int(status.progress() * 100)}%")
        print(f"Downloaded file to {self.destination_folder}/{file_name}")

    def list_and_choose_file_for_download(self):
        selected_file = list_and_choose_file(self.service)
        if selected_file:
            self.download_file_by_name(selected_file['name'])

# List operation
class ListOperation(StorageOperation):
    def __init__(self, credentials):
        super().__init__(credentials)

    def execute(self):
        # List files in Google Drive's root directory
        results = self.service.files().list(
            q="'root' in parents",
            fields="files(id, name, mimeType, modifiedTime)"
        ).execute()
        items = results.get('files', [])

        if not items:
            print("No files found in Google Drive.")
            return

        # Display file details (name, type, last modified date)
        print("Listing files in root directory:")
        for item in items:
            name = item['name']
            mime_type = item['mimeType']
            modified_time = item['modifiedTime']
            print(f"Name: {name}, Type: {mime_type}, Last Modified: {modified_time}")


class RemoveOperation(StorageOperation):
    def __init__(self, credentials, filename=None):
        super().__init__(credentials)
        self.filename = filename

    def execute(self):
        if self.filename:  # Direct deletion by filename
            self.remove_file_by_name(self.filename)
        else:  # No filename provided, list files and ask user to choose
            self.list_and_choose_file_for_removal()

    def remove_file_by_name(self, file_name):
        # Find the file in the root directory by filename
        query = f"name = '{file_name}' and 'root' in parents"
        results = self.service.files().list(q=query, fields="files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            print(f"File with name {file_name} not found in Google Drive.")
            return

        # Delete the first matching file
        file_id = items[0]['id']
        self.service.files().delete(fileId=file_id).execute()
        print(f"Removed file with name: {file_name} (ID: {file_id})")

    def list_and_choose_file_for_removal(self):
        selected_file = list_and_choose_file(self.service)
        if selected_file:
            file_id = selected_file['id']
            self.service.files().delete(fileId=file_id).execute()
            print(f"Removed file with name: {selected_file['name']} (ID: {file_id})")