import deepl

class EmailTranslator:
    def __init__(self, api_key):
        """Initialize the EmailTranslator with a DeepL API key."""
        self.translator = deepl.Translator(api_key)

    def translate_email(self, text, target_language="EN-US"):
        """Translate a single piece of text into the specified target language."""
        # Define valid target languages supported by DeepL
        valid_languages = ["EN-US", "DE", "FR", "IT", "ES", "PL", "NL", "PT", "RU", "JA", "ZH"]

        if target_language not in valid_languages:
            raise ValueError(f"Langue cible invalide. Langues valides: {', '.join(valid_languages)}")

        try:
            # Translate the text using DeepL
            result = self.translator.translate_text(text, target_lang=target_language)
            return result.text
        except deepl.exceptions.RequestError as e:
            print(f"Erreur de demande à l'API DeepL: {e}")
            return None
        except Exception as e:
            print(f"Erreur inattendue: {e}")
            return None

    def translate_email_subject_and_body(self, subject, body, target_language="EN-US"):
        """Translate both the subject and the body of an email."""
        translated_subject = None
        translated_body = None

        if subject.strip():  # Translate the subject if it exists
            translated_subject = self.translate_email(subject, target_language)

        if body.strip():  # Translate the body if it exists
            translated_body = self.translate_email(body, target_language)

        return {
            "translated_subject": translated_subject,
            "translated_body": translated_body
        }
