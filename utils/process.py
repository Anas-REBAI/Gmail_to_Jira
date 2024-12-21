import threading
import time
import logging
from models.email_parser import EmailParser
from models.email_classifier import EmailClassifier
from models.email_translator import EmailTranslator
from utils.predict import predict_translate_and_create_jira_issue
from config.settings import EMAIL_USER, EMAIL_PASS, IMAP_SERVER, DEEPL_API_KEY

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

stop_event = threading.Event()

# Main function to execute periodically
def process_emails():
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

        # Predict priority, Translate email and create jira issue
        predict_translate_and_create_jira_issue(emails, classifier, translator)

        logger.info("Email processing completed.")
    except Exception as e:
        logger.error(f"Error during email processing: {e}")

# Periodic task in a thread
def run_periodic_task():
    while not stop_event.is_set():
        process_emails()
        time.sleep(60)

# Background task
def start_background_task():
    thread = threading.Thread(target=run_periodic_task)
    thread.daemon = True
    thread.start()

# Cleanly stop the thread
def shutdown_task():
    stop_event.set()