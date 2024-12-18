from config.settings import EMAIL_USER, EMAIL_PASS, IMAP_SERVER, DEEPL_API_KEY, JIRA_URL, JIRA_USER, JIRA_API_TOKEN, JIRA_PROJECT_KEY, RECEIVER_EMAIL
from models.email_parser import EmailParser
from models.email_classifier import EmailClassifier
from models.email_translator import EmailTranslator
from models.jira_integration import JiraIntegration
from utils.predict import read_and_translate_important_emails
from utils.sendEmail import send_email 


if __name__ == "__main__":

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
        priority = classifier.predict_priority(body)

        if priority == "high":
            # Verify keywords in the subject line
            keywords_found_in_subject = [keyword for keyword in classifier.priority_keywords["high"] if keyword in subject.lower()]
            if keywords_found_in_subject:
                print(f"Processing high-priority email from {sender} with subject: {subject}")

                # Translate Email
                translated_body = translator.translate_email(body, "EN")

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