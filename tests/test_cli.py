import unittest
from unittest.mock import patch
from functions.cli import CLI
import sys

class TestCLI(unittest.TestCase):

    @patch('sys.argv', new=['googD.py', '--upload', 'file.txt'])
    def test_parse_arguments_upload(self):
        cli = CLI()
        args = cli.parse_arguments()
        self.assertTrue(args.upload)
        self.assertEqual(args.upload, 'file.txt')

    @patch('sys.argv', new=['googD.py', '--list'])
    def test_parse_arguments_list(self):
        cli = CLI()
        args = cli.parse_arguments()
        self.assertTrue(args.list)

    @patch('sys.argv', new=['googD.py', '--download', '--file', 'file.txt'])
    def test_parse_arguments_download(self):
        cli = CLI()
        args = cli.parse_arguments()
        self.assertTrue(args.download)
        self.assertEqual(args.file, 'file.txt')

if __name__ == '__main__':
    unittest.main()
