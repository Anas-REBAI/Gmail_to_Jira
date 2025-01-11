from utils.sendEmail import send_email
from models.jira_integration import JiraIntegration
from config.settings import EMAIL_USER, EMAIL_PASS, JIRA_URL, JIRA_API_TOKEN, JIRA_PROJECT_KEY

def predict_translate_and_create_jira_issue(emails, classifier, translator):
    """Filter, display, translate emails based on their priority and create issue jira."""

    # Initialize Jira Integration
    jira = JiraIntegration(JIRA_URL, EMAIL_USER, JIRA_API_TOKEN)

    if emails:  # Check if there are emails to process
        print(f"\nEmails List:\n")

        for subject, sender, body in emails:
            if not subject.strip() or not body.strip():
                print(f"Skipping email from {sender} with empty subject or body.")
                send_email(
                    sender_email=EMAIL_USER,
                    sender_password=EMAIL_PASS,
                    receiver_email=EMAIL_USER,
                    subject="Email Notification",
                    body=f"Skipping email from {sender} with empty subject or body. Error creating Jira task."
                )
                continue

            # Translate the subject and body if necessary
            translations = translator.translate_email_subject_and_body(subject, body, target_language="EN-US")
            translated_subject = translations.get("translated_subject", subject)
            translated_body = translations.get("translated_body", body)

            if not translated_subject or not translated_body:
                translated_subject = subject
                translated_body = body

            # Classify the emails
            priority = classifier.predict_priority(translated_subject, translated_body)

            # Display basic email information and the translated content
            print(f"\nFrom: {sender}\nSubject (original): {subject}\nSubject (Translated): {translated_subject}")
            print(f"Priority: {priority}\nBody (original): {body}\nBody (Translated): {translated_body}")

            # Create a Jira task
            jira.create_task(
                project_key=JIRA_PROJECT_KEY,
                summary=f"[{priority}] {translated_subject}",
                description=f"Sender: {sender}\n\nBody:\n{translated_body}",
                priority=priority
            )
