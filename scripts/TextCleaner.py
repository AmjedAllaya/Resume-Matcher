import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import string

class TextCleaner:

    def __init__(self, raw_text):
        self.stopwords_set = set(stopwords.words('english') + list(string.punctuation))
        self.lemmatizer = WordNetLemmatizer()
        self.raw_input_text = raw_text

    def clean_text(self) -> str:
        try:
            tokens = word_tokenize(self.raw_input_text.lower())
            tokens = [token for token in tokens if token not in self.stopwords_set]
            tokens = [self.lemmatizer.lemmatize(token) for token in tokens]
            cleaned_text = ' '.join(tokens)
            return cleaned_text
        except Exception as e:
            # Handle exceptions gracefully, log the error, and return the original text.
            print(f"Error during text cleaning: {str(e)}")
            return self.raw_input_text

    def remove_special_characters(self, text: str) -> str:
        """
        Remove special characters and punctuation from the text.
        """
        try:
            text = text.translate(str.maketrans('', '', string.punctuation))
            return text
        except Exception as e:
            # Handle exceptions gracefully, log the error, and return the original text.
            print(f"Error removing special characters: {str(e)}")
            return text

    def remove_numbers(self, text: str) -> str:
        """
        Remove numbers from the text.
        """
        try:
            text = ''.join(word for word in text if not word.isdigit())
            return text
        except Exception as e:
            # Handle exceptions gracefully, log the error, and return the original text.
            print(f"Error removing numbers: {str(e)}")
            return text
