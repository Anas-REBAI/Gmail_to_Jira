import threading
import time
import logging
from models.email_parser import EmailParser
from models.email_classifier import EmailClassifier
from models.email_translator import EmailTranslator
from utils.predict import predict_translate_and_create_jira_issue
from config.settings import EMAIL_USER, EMAIL_PASS, IMAP_SERVER, DEEPL_API_KEY

# Logger configuration
logger = logging.getLogger(__name__)

# Thread control
stop_event = threading.Event()

def process_emails():
    """Main logic for processing emails."""
    try:
        logger.info("Starting email processing...")
        
        # Initialize Components
        email_parser = EmailParser(EMAIL_USER, EMAIL_PASS, IMAP_SERVER)
        classifier = EmailClassifier()
        translator = EmailTranslator(DEEPL_API_KEY)

        # Connect to gmail
        email_parser.connect()
        
        # Fetch Emails
        emails = email_parser.fetch_emails()

        # Predict Priority, Translate email and create Jira issue
        predict_translate_and_create_jira_issue(emails, classifier, translator)

        logger.info("Email processing completed.")
    except Exception as e:
        logger.error(f"Error during email processing: {e}")

def run_periodic_task():
    """Thread loop to periodically execute the email processing."""
    while not stop_event.is_set():
        process_emails()
        time.sleep(60)

def start_background_task():
    """Start the background thread."""
    thread = threading.Thread(target=run_periodic_task, daemon=True)
    thread.start()

def stop_background_task():
    """Stop the background thread."""
    stop_event.set()
