def read_and_translate_important_emails(emails, classifier, translator):
    """Filter, display, and translate important emails based on keywords."""
    print("\nImportant Emails:")
    for subject, sender, body in emails:
        priority = classifier.predict_priority(body)
        if priority == "high":
            # Extract keywords matched
            keywords_found = [keyword for keyword in classifier.priority_keywords["high"] if keyword in body.lower()]
            if keywords_found:  # Ensure the body contains at least one high-priority keyword
                translated_body = translator.translate_email(body, "EN")
                print(f"\nFrom: {sender}\nSubject: {subject}\nKeywords Found: {', '.join(keywords_found)}\nBody (Translated): {translated_body}\n")
            else:
                print(f"\nFrom: {sender}\nSubject: {subject}\nNo high-priority keywords found in the body.\n")