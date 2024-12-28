import imaplib
import email
import os
from email.header import decode_header


def connect_to_gmail(email_address, password):
    """Connect to Gmail IMAP server with better error handling"""
    try:
        # Connect to Gmail IMAP server
        print(f"Attempting to connect to imap.gmail.com...")
        imap_server = "imap.gmail.com"
        imap = imaplib.IMAP4_SSL(imap_server)

        print(f"Attempting to login with {email_address}...")
        imap.login(email_address, password)
        print("Successfully logged in!")
        return imap
    except imaplib.IMAP4.error as e:
        print("\nIMAP Error occurred:")
        print(f"- Error message: {str(e)}")
        print("\nPossible solutions:")
        print("1. Make sure you're using an App Password if 2FA is enabled")
        print("2. Enable 'Less secure app access' if not using 2FA")
        print("3. Make sure IMAP is enabled in Gmail settings")
        raise
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
        raise


def try_decode(encoded_text, encodings=["utf-8", "latin-1", "ascii", "iso-8859-1"]):
    """Try multiple encodings to decode text"""
    for encoding in encodings:
        try:
            return encoded_text.decode(encoding)
        except UnicodeDecodeError:
            continue
    return None


def find_sent_folder(imap):
    """Find the correct sent folder name"""
    print("Looking for sent mail folder...")

    # List all available folders
    _, folders = imap.list()

    # Common Gmail sent folder names, including Turkish version
    possible_names = [
        '"[Gmail]/Sent Mail"',
        "[Gmail]/Sent Mail",
        '"[Google Mail]/Sent Mail"',
        "[Google Mail]/Sent Mail",
        "Sent",
        '"Sent"',
        '"[Gmail]/G&APY-nderilmi&AV8- Postalar"',  # Turkish version
        "[Gmail]/G&APY-nderilmi&AV8- Postalar",  # Turkish version without quotes
    ]

    for folder in folders:
        folder_name = folder.decode().split('" ')[-1].strip('"')  # Changed split pattern
        print(f"Found folder: {folder_name}")

    # Try each possible name
    for folder_name in possible_names:
        try:
            status, messages = imap.select(folder_name)
            if status == "OK":
                print(f"Successfully selected folder: {folder_name}")
                return True
        except Exception as e:
            print(f"Failed to select {folder_name}: {str(e)}")
            continue

    return False


def download_emails(imap, output_dir="raw_emails", max_emails=5000):
    """Download sent emails from Gmail via IMAP"""
    try:
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Find and select the sent folder
        if not find_sent_folder(imap):
            raise Exception("Could not find sent mail folder")

        # Search for all sent emails
        print("Searching for sent emails...")
        _, message_numbers = imap.search(None, "ALL")

        # Get message numbers and limit to max_emails, starting from newest
        message_nums = message_numbers[0].split()
        message_nums.reverse()  # Reverse to get newest first
        total_available = len(message_nums)
        message_nums = message_nums[:max_emails]  # Take first max_emails
        total_messages = len(message_nums)

        print(f"Found {total_available} sent emails total.")
        print(f"Downloading the {total_messages} most recent emails...")

        emails = []
        successful_downloads = 0

        for i, num in enumerate(message_nums, 1):
            if i % 100 == 0:  # Progress update every 100 emails
                print(f"Processing email {i}/{total_messages} ({successful_downloads} successful)...")

            try:
                # Fetch email message by ID
                _, msg_data = imap.fetch(num, "(RFC822)")
                email_body = msg_data[0][1]
                message = email.message_from_bytes(email_body)

                # Try to get the email content type
                content_type = message.get_content_type()

                # Initialize body text
                body_text = ""

                # Get email content
                if message.is_multipart():
                    for part in message.walk():
                        content_type = part.get_content_type()
                        if content_type == "text/plain" or content_type == "text/html":
                            try:
                                payload = part.get_payload(decode=True)
                                if payload:
                                    decoded = try_decode(payload)
                                    if decoded:
                                        body_text += decoded + "\n"
                            except Exception as e:
                                print(f"Error decoding part of email {i}: {str(e)}")
                else:
                    try:
                        payload = message.get_payload(decode=True)
                        if payload:
                            decoded = try_decode(payload)
                            if decoded:
                                body_text = decoded

                    except Exception as e:
                        print(f"Error decoding email {i}: {str(e)}")

                # Only append if we got some content
                if body_text.strip():
                    successful_downloads += 1
                    emails.append(body_text)

            except Exception as e:
                print(f"Error processing email {i}: {str(e)}")
                continue

        print(f"\nDownload complete!")
        print(f"Successfully downloaded {len(emails)} emails with content")
        print(f"Success rate: {(len(emails)/total_messages)*100:.1f}%")

        # Debug: print first few characters of first few emails
        print("\nSample content from first few emails:")
        for i, email_text in enumerate(emails[:3]):
            if email_text:
                preview = email_text[:100].replace("\n", " ")
                print(f"\nEmail {i+1}: {preview}...")

        return emails

    except Exception as e:
        print(f"Error downloading emails: {str(e)}")
        raise


if __name__ == "__main__":
    email_address = input("Enter your email address: ")
    password = input("Enter your password or app password: ")

    imap = connect_to_gmail(email_address, password)
    emails = download_emails(imap)
    imap.logout()
