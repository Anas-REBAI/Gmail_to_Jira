import email
from email.header import decode_header
from imapclient import IMAPClient

# Email Parsing and Extraction
class EmailParser:
    def __init__(self, email_user, email_password, imap_server):
        self.user = email_user
        self.password = email_password
        self.server = imap_server
        self.connection = None

    def connect(self):
        """Establish a secure connection to the IMAP server."""
        try:
            self.connection = IMAPClient(self.server, ssl=True)
            self.connection.login(self.user, self.password)
            print("Connected and logged in successfully!")
        except Exception as e:
            print(f"Error connecting to server: {e}")

    def fetch_emails(self):
        """Fetch unread emails from the INBOX folder."""
        try:
            if not self.connection:
                raise Exception("IMAP connection is not established. Call connect() first.")
            self.connection.select_folder("INBOX")
            # Filter for UNREAD emails
            messages = self.connection.search(["UNSEEN"])
            print(f"Found {len(messages)} unread email(s).")
            if not messages:
                return []  # No unread emails

            emails = []
            for msg_id in messages:
                raw_message = self.connection.fetch(msg_id, ["RFC822"])
                for response in raw_message.values():
                    msg = email.message_from_bytes(response[b"RFC822"])
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        try:
                            subject = subject.decode(encoding if encoding else "utf-8")
                        except (UnicodeDecodeError, LookupError):
                            subject = subject.decode("latin1")  # Fallback to Latin-1
                    sender = msg.get("From")
                    body = None
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                try:
                                    body = part.get_payload(decode=True).decode(part.get_content_charset() or "utf-8")
                                except (UnicodeDecodeError, LookupError):
                                    body = part.get_payload(decode=True).decode("latin1")  # Fallback to Latin-1
                                break
                    else:
                        try:
                            body = msg.get_payload(decode=True).decode(msg.get_content_charset() or "utf-8")
                        except (UnicodeDecodeError, LookupError):
                            body = msg.get_payload(decode=True).decode("latin1")  # Fallback to Latin-1
                    if body:
                        emails.append((subject, sender, body))
            return emails
        except Exception as e:
            print(f"Error fetching emails: {e}")
            return []