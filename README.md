# stracProject

# Google Cloud CLI Tool Overview

This is a command-line tool to interact with Google Cloud Storage using OAuth2 authentication. The tool supports four main operations:

- `list` - List files in Google Cloud Storage.
- `upload` - Upload a file to Google Cloud Storage.
- `download` - Download a file from Google Cloud Storage.
- `delete` - Delete a file from Google Cloud Storage.
---

## Installation
Provide steps to install or set up the tool.

1. Install Python for your machine type and activate the virtual environment

```bash
python -m venv venv
source venv/bin/activate
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client pytest

deactivate (optional when done)
```

## Usage

#### 1. **List Files in Google Drive**
List all files in your Google Drive's root directory. Display file
names, types, and last modified dates.

```bash
python googD.py --list
```

#### 2. Upload a File
Upload a file to Google Drive. Optionally, you can specify a folder name to upload the file to a specific folder. If the folder does not exist, it will be created.

```bash
python googD.py --upload path/to/local/file.txt --folder "Folder Name"
```

--upload (Required): Path to the file you want to upload. (relative or absolute)

--folder (Optional): Name of the folder to upload to. If not provided, the file will be uploaded to the root directory.

### 3. Download a File
Download a file from Google Drive. You can either specify the file name directly or list the available files and choose one.

Download a Specific File:

```bash
python googD.py --download --file filename.txt
```
List and Choose a File to Download:
```bash
python googD.py --download
```
--file (Optional): The exact name of the file you wish to download. If not provided, you will be prompted to select a file from a list of available files in your Google Drive.

### 4. Delete a File
Delete a specific file from Google Drive. You can either specify the file name directly or list the available files and choose one to delete.

Delete a Specific File:

```bash
python googD.py --delete --file filename.txt
```
List and Choose a File to Delete:

```bash
python googD.py --delete
```
--file (Optional): The exact name of the file you wish to delete. If not provided, you will be prompted to select a file from a list of available files in your Google Drive.

### 5. Run unit/integration tests

To run the tests, make sure you are already authorized by running

```bash
python googD.py --list
```
Then can run tests.
```bash
pytest -s -v
```

Remove token.json after since the tests invalidate it.

## Google OAuth 2.0 Authentication Setup

To use OAuth 2.0 authentication with Google Drive, follow these steps to obtain the `client_secrets.json` file:

### 1. Download the `client_secrets.json` File

You need to create a Google Cloud project and enable the necessary APIs for OAuth authentication. Follow these steps to obtain the `client_secrets.json` file:

- Go to the [Google Developer Console](https://console.developers.google.com/).
  
- **Create a new project** (or use an existing one).
  
- **Enable the Google Drive API**:
  - In the dashboard, click on `Enable APIs and Services`.
  - Search for `Google Drive API` and enable it.

- **Create OAuth 2.0 Credentials**:
  - In the API & Services > Credentials section under Google Drive API, click `Create Credentials`.
  - Select `OAuth 2.0 Client ID`.
  - Choose `(Desktop app)`.
  - Set a name for your OAuth 2.0 client (e.g., `googD OAuth`).
  - Click `Create`, and you'll be able to download the `client_secrets.json` file.

### 2. Place the `client_secrets.json` File

Once downloaded, **move the `client_secrets.json` file** to the root of your project directory (where your script is located).


## Assumptions/Notes

- list,download,delete doesn't support other folders, it just lists the root folder (this was not listed in specification)



