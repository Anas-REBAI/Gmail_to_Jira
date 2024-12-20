from flask import Flask
import threading
import time
from models.email_parser import EmailParser
from models.email_classifier import EmailClassifier
from models.email_translator import EmailTranslator
from models.jira_integration import JiraIntegration
from utils.predict import read_and_translate_important_emails
from utils.sendEmail import send_email
from config.settings import EMAIL_USER, EMAIL_PASS, IMAP_SERVER, DEEPL_API_KEY, JIRA_URL, JIRA_USER, JIRA_API_TOKEN, JIRA_PROJECT_KEY, RECEIVER_EMAIL

# ***************** Flask application ************************************
app = Flask(__name__)

# Fonction principale à exécuter périodiquement
def process_emails():
    try:
        # Initialize Components
        email_parser = EmailParser(EMAIL_USER, EMAIL_PASS, IMAP_SERVER)
        email_parser.connect()

        classifier = EmailClassifier()
        translator = EmailTranslator(DEEPL_API_KEY)
        jira = JiraIntegration(JIRA_URL, JIRA_USER, JIRA_API_TOKEN)

        # Fetch Emails
        emails = email_parser.fetch_emails()

        # Display and Translate Important Emails
        read_and_translate_important_emails(emails, classifier, translator)

        for subject, sender, body in emails:
            priority = classifier.predict_priority(subject, body)

            if priority == "high":
                # Verify keywords in the subject line
                keywords_found_in_subject = [
                    keyword for keyword in classifier.priority_keywords["high"] if keyword in subject.lower()
                ]
                if keywords_found_in_subject:
                    print(f"Processing high-priority email from {sender} with subject: {subject}")

                    # Translate Email
                    translated_body = translator.translate_email(body, "EN-US")

                    # Create JIRA Task
                    jira_task = jira.create_task(JIRA_PROJECT_KEY, subject, translated_body)
                    print(f"Created JIRA task: {jira_task.key}")

                    # Send Notification Email
                    send_email(
                        sender_email=EMAIL_USER,
                        sender_password=EMAIL_PASS,
                        receiver_email=RECEIVER_EMAIL,
                        subject="High Priority Email Notification",
                        body=f"High priority email received from {sender} with subject: {subject}."
                    )
                else:
                    print(f"High-priority email detected but no keywords found in the subject: {subject}")
    except Exception as e:
        print(f"Error during email processing: {e}")

# Tâche périodique en thread
def run_periodic_task():
    while True:
        process_emails()
        time.sleep(60)

# La tâche en arrière-plan
def start_background_task():
    thread = threading.Thread(target=run_periodic_task)
    thread.daemon = True
    thread.start()

# ***************** Main execution ************************************
if __name__ == "__main__":  
    start_background_task()
    app.run(host="0.0.0.0", port=5000)