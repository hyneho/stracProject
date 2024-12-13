import unittest
import subprocess

class TestIntegration(unittest.TestCase):

    def run_cli(self, *args):
        """Helper method to run the CLI with arguments and capture the output."""
        result = subprocess.run(
            ['python3', 'googD.py', *args],
            capture_output=True,
            text=True
        )
        print(result.stdout)  # Ensure this output is printed to the console
        return result

    def test_upload(self):
        """Test the upload operation with valid arguments."""
        print("Running upload test...")
        result = self.run_cli('--upload', 'test.txt', '--folder', 'test_folder')
        print(result.stdout)  # Ensure the result is printed

    def test_download(self):
        """Test the download operation with valid arguments."""
        print("Running download test...")
        result = self.run_cli('--download', '--file', 'test.txt')
        print(result.stdout)  # Ensure the result is printed

    def test_list(self):
        """Test the list operation to list available files."""
        print("Running list test...")
        result = self.run_cli('--list')
        print(result.stdout)  # Ensure the result is printed

    def test_delete(self):
        """Test the delete operation with a test file."""
        print("Running delete test...")
        result = self.run_cli('--delete', '--file', 'test.txt')
        print(result.stdout)  # Ensure the result is printed

if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)  # Make sure verbosity is set to 2 to show output
