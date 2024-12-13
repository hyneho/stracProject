import argparse

class CLI:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Google Drive CLI Tool")
        self.parser.add_argument('--list', action='store_true', help="List files in Google Drive")
        self.parser.add_argument('--upload', help="Upload a file to Google Drive")
        self.parser.add_argument('--delete', help="Delete a file from Google Drive", action='store_true')
        self.parser.add_argument('--download', help="Download a file from Google Drive", action='store_true')
        self.parser.add_argument('--folder', help="Google Drive folder name to upload file to", default=None)
        self.parser.add_argument('--file', help="File name to download", default=None)

    def parse_arguments(self):
        return self.parser.parse_args()

