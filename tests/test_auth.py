import os
import pickle
import unittest
from unittest import mock
from unittest.mock import patch, Mock, MagicMock

from google.auth.credentials import AnonymousCredentials

from functions.auth import Authenticator


class TestAuthenticator(unittest.TestCase):

    @patch('functions.auth.pickle.load', return_value=None)
    @patch('functions.auth.pickle.dump')
    @patch('functions.auth.InstalledAppFlow.from_client_secrets_file')
    @patch('functions.auth.Request')
    def test_authenticate_new_user(self, mock_request, mock_flow, mock_pickle_dump, mock_pickle_load):
        # Mock the OAuth flow to simulate a successful login
        mock_creds = mock.Mock()
        mock_creds.valid = True
        mock_flow.return_value.run_local_server.return_value = mock_creds

        auth = Authenticator()
        creds = auth.authenticate()

        self.assertEqual(creds, mock_creds)
        mock_pickle_dump.assert_called_once()

    @patch('pickle.load')
    @patch.object(Authenticator, 'perform_oauth_flow')
    def test_authenticate_existing_valid_creds(self, mock_perform_oauth_flow, mock_pickle_load):
        # Create a mock credentials object
        mock_creds = MagicMock(spec=AnonymousCredentials)

        # Mock the attributes that the 'authenticate' method accesses
        mock_creds.expired = False  # Simulate valid credentials
        mock_creds.valid = True  # Simulate valid credentials
        mock_creds.refresh_token = "mock_refresh_token"  # Simulate a valid refresh token

        # Mock pickle.load to return the mock credentials
        mock_pickle_load.return_value = mock_creds

        # Simulate that the credentials file exists and contains valid credentials
        auth = Authenticator()
        creds = auth.authenticate()

        # Assert that the credentials returned match the mocked credentials
        self.assertEqual(creds, mock_creds)

        # Ensure that perform_oauth_flow was not called since credentials were valid
        mock_perform_oauth_flow.assert_not_called()


    @patch('pickle.load', side_effect=pickle.PickleError)  # Mock pickle.load to simulate an invalid token
    @patch.object(Authenticator, 'perform_oauth_flow')  # Mock perform_oauth_flow to avoid real OAuth flow
    def test_authenticate_invalid_creds(self, mock_perform_oauth_flow, mock_pickle_load):
        # Simulate that the credentials file doesn't exist or is invalid
        if os.path.exists(Authenticator.CREDENTIALS_FILE):
            os.remove(Authenticator.CREDENTIALS_FILE)  # Ensure the token.json file is removed or invalid

        # Make sure the mock for perform_oauth_flow returns some fake credentials
        mock_perform_oauth_flow.return_value = "mocked_credentials"

        # Create an Authenticator instance and call authenticate
        auth = Authenticator()
        credentials = auth.authenticate()

        # Assert that the mock for perform_oauth_flow was called once
        mock_perform_oauth_flow.assert_called_once()

        # Check that the returned credentials match what we mocked
        self.assertEqual(credentials, "mocked_credentials")


if __name__ == '__main__':
    unittest.main()
