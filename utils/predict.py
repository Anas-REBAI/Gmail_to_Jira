from utils.sendEmail import send_email
from models.jira_integration import JiraIntegration
from config.settings import EMAIL_USER, EMAIL_PASS, JIRA_URL, JIRA_API_TOKEN, JIRA_PROJECT_KEY

def predict_translate_and_create_issueJira(emails, classifier, translator):
    """Filter, display, translate emails based on their priority and create issue jira."""

    # Initialize Jira Integration
    jira = JiraIntegration(JIRA_URL, EMAIL_USER, JIRA_API_TOKEN)

    if emails:  # Vérifiez qu'il y a des emails à afficher
        print(f"\nEmails List:\n")

    for subject, sender, body in emails:
        if not subject.strip() or not body.strip():
            print(f"Skipping email from {sender} with empty subject or body.")
            continue

        # Classification des emails
        priority = classifier.predict_priority(subject, body)

        # Afficher les informations de base de l'email
        print(f"\nFrom: {sender}\nSubject: {subject}\nPriority: {priority}")

        # Traduction de l'email si nécessaire
        translated_body = None
        if body.strip():
            try:
                translated_body = translator.translate_email(body, "EN-US")
            except Exception as e:
                translated_body = f"Translation error: {e}"

        # Afficher le corps traduit
        print(f"Body (Translated): {translated_body}\n")

        # Create JIRA Task
        jira.create_task(
            project_key=JIRA_PROJECT_KEY,
            summary=f"[{priority}] Email: {subject}",
            description=f"Sender: {sender}\n\nBody:\n{translated_body}",
            priority=priority
        )

        # Envoyer un email de notification uniquement pour les priorités élevées
        if priority.lower() in ["high"]:
            send_email(
                sender_email=EMAIL_USER,
                sender_password=EMAIL_PASS,
                receiver_email=EMAIL_USER,
                subject="Email Notification",
                body=f"{priority} Email received from {sender} with subject: {subject}.\nEmail Body: {translated_body}"
            )
