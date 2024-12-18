import deepl

class EmailTranslator:
    def __init__(self, api_key):
        self.translator = deepl.Translator(api_key)

    def translate_email(self, email_body, target_language="EN"):
        result = self.translator.translate_text(email_body, target_lang=target_language)
        return result.text
