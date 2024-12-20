def read_and_translate_important_emails(emails, classifier, translator):
    """Filter, display, and translate emails based on their priority."""

    for subject, sender, body in emails:
        # Classification des emails
        priority = classifier.predict_priority(subject, body)

        print(f"\nEmails List:\n")

        # Afficher les informations de base de l'email
        print(f"\nFrom: {sender}\nSubject: {subject}\nPriority: {priority}")

        # Traduction de l'email
        try:
            translated_body = translator.translate_email(body, "EN-US")
        except Exception as e:
            translated_body = f"Translation error: {e}"

        # Afficher le corps traduit
        print(f"Body (Translated): {translated_body}\n")

