import deepl

class EmailTranslator:
    def __init__(self, api_key):
        """Initialise le traducteur avec la clé API DeepL."""
        self.translator = deepl.Translator(api_key)

    def translate_email(self, email_body, target_language="EN-US"):
        """Traduit le texte de l'email dans la langue cible."""
        # Vérification que la langue cible est valide
        valid_languages = ["EN-US", "DE", "FR", "IT", "ES", "PL", "NL", "PT", "RU", "JA", "ZH"]
        if target_language not in valid_languages:
            raise ValueError(f"Langue cible invalide. Langues valides: {', '.join(valid_languages)}")

        try:
            # Traduction du texte
            result = self.translator.translate_text(email_body, target_lang=target_language)
            return result.text
        except deepl.exceptions.RequestError as e:
            print(f"Erreur de demande à l'API DeepL: {e}")
            return None
        except Exception as e:
            print(f"Erreur inattendue: {e}")
            return None

