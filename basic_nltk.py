import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.probability import FreqDist
import string

# Download NLTK resources (run this only once)
nltk.download('punkt')
nltk.download('stopwords')

# Sample text for NLP processing
text = """
Natural Language Processing (NLP) is a subfield of artificial intelligence that focuses on the interaction
between computers and humans through natural language. NLP techniques can be used for various tasks
like text classification, sentiment analysis, machine translation, and more.
"""

# Tokenization: Break the text into words and sentences
words = word_tokenize(text)
sentences = sent_tokenize(text)

# Removing stopwords and punctuation
stop_words = set(stopwords.words('english'))
filtered_words = [word.lower() for word in words if word.lower() not in stop_words and word not in string.punctuation]

# Stemming: Reducing words to their root form
stemmer = PorterStemmer()
stemmed_words = [stemmer.stem(word) for word in filtered_words]

# Frequency distribution of words
fdist = FreqDist(stemmed_words)

# Print the results
print("Original Text:")
print(text)

print("\nTokenized Words:")
print(words)

print("\nTokenized Sentences:")
print(sentences)

print("\nWords after Removing Stopwords and Punctuation:")
print(filtered_words)

print("\nStemmed Words:")
print(stemmed_words)

print("\nWord Frequency Distribution:")
print(fdist.most_common(10))
