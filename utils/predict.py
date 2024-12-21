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
                continue

            # Classify the emails
            priority = classifier.predict_priority(subject, body)

            # Display basic email information
            print(f"\nFrom: {sender}\nSubject: {subject}\nPriority: {priority}")

            # Translate the email body if necessary
            translated_body = None
            if body.strip():
                try:
                    translated_body = translator.translate_email(body, "EN-US")
                except Exception as e:
                    translated_body = f"Translation error: {e}"

            # Display the translated body
            print(f"Body (Translated): {translated_body}\n")

            # Create a Jira task
            jira.create_task(
                project_key=JIRA_PROJECT_KEY,
                summary=f"[{priority}] Email: {subject}",
                description=f"Sender: {sender}\n\nBody:\n{translated_body}",
                priority=priority
            )

            # Send a notification email only for high-priority emails
            if priority.lower() in ["high"]:
                send_email(
                    sender_email=EMAIL_USER,
                    sender_password=EMAIL_PASS,
                    receiver_email=EMAIL_USER,
                    subject="Email Notification",
                    body=f"{priority} Email received from {sender} with subject: {subject}.\nEmail Body: {translated_body}"
                )
