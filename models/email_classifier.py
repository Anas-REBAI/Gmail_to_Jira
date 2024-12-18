# Machine Learning Email Classifier
class EmailClassifier:
    def __init__(self):
        self.priority_keywords = {
            "high": ["urgent", "asap", "important", "action required", "deadline"],
            "medium": ["follow up", "reminder", "check", "update"],
            "low": ["info", "newsletter", "FYI", "no action required"]
        }

    def classify_by_keywords(self, email_body):
        """Classify email priority based on the presence of keywords."""
        email_body_lower = email_body.lower()  # Convert email body to lowercase for case-insensitive matching

        for priority, keywords in self.priority_keywords.items():
            for keyword in keywords:
                if keyword in email_body_lower:
                    return priority  # Return the priority as soon as a match is found

        return "low"  # Default to 'low' priority if no keywords are matched

    def predict_priority(self, email_body):
        """Wrapper to integrate keyword classification into ML-based prediction if needed."""
        return self.classify_by_keywords(email_body)