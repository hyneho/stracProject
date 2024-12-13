from functions.auth import Authenticator
from functions.storage_operations import UploadOperation, DownloadOperation, ListOperation, RemoveOperation
from functions.cli import CLI

def main():
    # Initialize CLI and parse arguments
    cli = CLI()
    args = cli.parse_arguments()

    # Authenticate
    auth = Authenticator()
    credentials = auth.authenticate()

    if not credentials:
        print("Authentication failed. Exiting.")
        return

    # Create operation based on arguments
    if args.list:
        operation = ListOperation(credentials)
    elif args.upload:
        operation = UploadOperation(credentials, args.upload, args.folder)
    elif args.download:
        if args.file:  # If --file is specified with the filename
            print(f"Downloading file: {args.file}")
            operation = DownloadOperation(credentials, args.file)
        else:  # If no file specified, list files and ask user to choose
            print("Listing files to choose a file for download...")
            operation = DownloadOperation(credentials)
    elif args.delete:  # If --delete is specified
        if args.file:  # If --file is specified with the filename
            print(f"Deleting file: {args.file}")
            operation = RemoveOperation(credentials, args.file)
        else:  # If no file specified, list files and ask user to choose
            print("Listing files to choose a file for deletion...")
            operation = RemoveOperation(credentials)
    else:
        raise ValueError("Invalid command")

    # Execute operation
    operation.execute()

if __name__ == '__main__':
    main()
