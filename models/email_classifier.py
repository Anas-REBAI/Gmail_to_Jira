from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

class EmailClassifier:
    def __init__(self):
        # Example training dataset with subject + body
        self.train_data = [
            ("Urgent! Please respond ASAP", "Please respond ASAP, deadline approaching", "high"),
            ("Reminder: Meeting tomorrow", "Don't forget the meeting at 3pm tomorrow", "medium"),
            ("Newsletter: Updates for this month", "Check out the latest updates in our newsletter", "low"),
            ("Deadline for report submission", "Please submit your report by the end of the day", "high"),
            ("Follow up on your last email", "Just following up on my previous message regarding the proposal", "medium"),
            ("FYI: New policies announced", "Important update regarding new company policies", "low")
        ]
        
        self.model = self._train_model()

    def _train_model(self):
        """Entraînement du modèle de machine learning avec TF-IDF et Naive Bayes."""
        # Combine the subject and body for each email
        texts = [f"{subject} {body}" for subject, body, label in self.train_data]
        labels = [label for subject, body, label in self.train_data]

        # Create and train the model
        model = make_pipeline(TfidfVectorizer(), MultinomialNB())
        model.fit(texts, labels)
        return model

    def predict_priority(self, subject, body):
        """Prédire la priorité en combinant le sujet et le corps de l'email."""
        combined_text = f"{subject} {body}"  # Combine subject and body
        predicted_priority = self.model.predict([combined_text])[0]  # Predict the priority
        return predicted_priority.capitalize()  # Capitalize the first letter of the priority
