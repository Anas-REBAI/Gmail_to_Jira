import email
from email.header import decode_header
from imapclient import IMAPClient

class EmailParser:
    def __init__(self, email_user, email_password, imap_server):
        self.user = email_user
        self.password = email_password
        self.server = imap_server
        self.connection = None

    # ***************** Connect to Gmail ************************************
    def connect(self):
        """Establish a secure connection to the IMAP server."""
        try:
            self.connection = IMAPClient(self.server, ssl=True)
            self.connection.login(self.user, self.password)
            print("Connected and logged in successfully!")
        except Exception as e:
            print(f"Error connecting to server: {e}")
            raise

    # ***************** Decode headers or content ************************************
    @staticmethod
    def decode_content(value, encoding):
        """Decode bytes or text with fallback to 'latin1'."""
        try:
            return value.decode(encoding if encoding else "utf-8")
        except (UnicodeDecodeError, LookupError):
            return value.decode("latin1")  # Fallback to Latin-1

    @staticmethod
    def extract_body(msg):
        """Extract the body from a message."""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain" and part.get_payload(decode=True):
                    encoding = part.get_content_charset()
                    return EmailParser.decode_content(part.get_payload(decode=True), encoding)
        else:
            encoding = msg.get_content_charset()
            return EmailParser.decode_content(msg.get_payload(decode=True), encoding)
        return None

    # ***************** Fetch emails ************************************
    def fetch_emails(self):
        """Fetch unread emails from the INBOX folder."""
        try:
            if not self.connection:
                raise Exception("IMAP connection is not established. Call connect() first.")
            
            self.connection.select_folder("INBOX")

            # Search for UNREAD emails from @esprit.tn only
            messages = self.connection.search(['UNSEEN', 'FROM', '@esprit.tn'])
            print(f"Found {len(messages)} unread email(s) from @esprit.tn")

            if not messages:
                return []  # No unread emails from this sender

            emails = []
            raw_messages = self.connection.fetch(messages, ["RFC822"])

            for msg_id, response in raw_messages.items():
                try:
                    msg = email.message_from_bytes(response[b"RFC822"])

                    # Decode subject
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = self.decode_content(subject, encoding)

                    # Extract sender and body
                    sender = msg.get("From")
                    body = self.extract_body(msg)

                    if body:
                        emails.append((subject, sender, body))
                except Exception as e:
                    print(f"Error processing email with ID {msg_id}: {e}")

            return emails
        except Exception as e:
            print(f"Error fetching emails: {e}")
            return []
