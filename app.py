from flask import Flask
import threading
import time
import logging
from models.email_parser import EmailParser
from models.email_classifier import EmailClassifier
from models.email_translator import EmailTranslator
from utils.predict import predict_translate_and_create_issueJira
from config.settings import EMAIL_USER, EMAIL_PASS, IMAP_SERVER, DEEPL_API_KEY

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Flask application 
app = Flask(__name__)

stop_event = threading.Event()

# Fonction principale à exécuter périodiquement
def process_emails():
    try:
        logger.info("Starting email processing...")
        
        # Initialize Components
        email_parser = EmailParser(EMAIL_USER, EMAIL_PASS, IMAP_SERVER)
        email_parser.connect()

        classifier = EmailClassifier()
        translator = EmailTranslator(DEEPL_API_KEY)

        # Fetch Emails
        emails = email_parser.fetch_emails()

        # Predict Priority, Translate email and create issue jira
        predict_translate_and_create_issueJira(emails, classifier, translator)

        logger.info("Email processing completed.")
    except Exception as e:
        logger.error(f"Error during email processing: {e}")

# Tâche périodique en thread
def run_periodic_task():
    while not stop_event.is_set():
        process_emails()
        time.sleep(60)

# La tâche en arrière-plan
def start_background_task():
    thread = threading.Thread(target=run_periodic_task)
    thread.daemon = True
    thread.start()

# Arrêter proprement le thread
@app.before_request
def shutdown_task():
    stop_event.set()

# Main execution
if __name__ == "__main__":
    start_background_task()
    try:
        app.run(host="0.0.0.0", port=5000)
    finally:
        stop_event.set()
