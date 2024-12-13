import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth import exceptions


class Authenticator:
    SCOPES = ['https://www.googleapis.com/auth/drive']
    CREDENTIALS_FILE = 'token.json'  # File to save user OAuth2 credentials
    CLIENT_SECRETS_FILE = 'client_secrets.json'  # File with OAuth2 client secrets

    def __init__(self):
        self.credentials = None

    def authenticate(self):
        """Authenticate using OAuth2 flow, either from existing credentials or by user login."""

        # Check if we already have valid credentials
        if os.path.exists(self.CREDENTIALS_FILE):
            try:
                with open(self.CREDENTIALS_FILE, 'rb') as token:
                    self.credentials = pickle.load(token)

                # If credentials are expired, refresh them
                if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                    self.credentials.refresh(Request())
                    self.save_credentials()
                elif not self.credentials or not self.credentials.valid:
                    raise exceptions.DefaultCredentialsError('Invalid credentials.')

            except (pickle.PickleError, exceptions.DefaultCredentialsError) as e:
                print("OAuth token is invalid or expired. Requesting new authentication...")
                self.credentials = None

        # If no valid credentials, or invalid/expired credentials, start new OAuth2 flow
        if not self.credentials:
            self.credentials = self.perform_oauth_flow()
            self.save_credentials()
        print("Successful Authentication")
        return self.credentials

    def perform_oauth_flow(self):
        """Perform OAuth2 flow and get credentials."""
        flow = InstalledAppFlow.from_client_secrets_file(
            self.CLIENT_SECRETS_FILE, self.SCOPES)

        creds = flow.run_local_server(port=0)  # Start the local server for OAuth2 callback
        return creds

    def save_credentials(self):
        """Save the OAuth2 credentials to a file for later use."""
        with open(self.CREDENTIALS_FILE, 'wb') as token:
            pickle.dump(self.credentials, token)
