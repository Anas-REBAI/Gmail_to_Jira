from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

class EmailClassifier:
    def __init__(self):
        # Exemple de jeu de données pour l'entraînement avec sujet + corps
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
        # On combine le sujet et le corps pour chaque email
        texts = [f"{subject} {body}" for subject, body, label in self.train_data]  # Combinaison du sujet et du corps
        labels = [label for subject, body, label in self.train_data]  # Récupérer les labels

        # Création et entraînement du modèle
        model = make_pipeline(TfidfVectorizer(), MultinomialNB())
        model.fit(texts, labels)  # Entraîner sur les textes combinés (sujet + corps)
        return model

    def predict_priority(self, subject, body):
        """Prédire la priorité en combinant le sujet et le corps de l'email."""
        combined_text = f"{subject} {body}"  # Combiner sujet et corps
        return self.model.predict([combined_text])[0]  # Prédire la priorité avec le modèle
