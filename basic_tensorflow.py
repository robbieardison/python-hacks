import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Sample movie reviews
positive_reviews = ["I loved the movie! It was fantastic.",
                    "Great acting and an engaging plot.",
                    "One of the best movies I've seen in years!"]

negative_reviews = ["Terrible film, a complete waste of time.",
                    "The acting was awful, and the plot was boring.",
                    "I couldn't stand this movie."]

# Labels: 1 for positive, 0 for negative
labels = [1, 1, 1, 0, 0, 0]

# Tokenization
tokenizer = Tokenizer(num_words=100, oov_token="<OOV>")
tokenizer.fit_on_texts(positive_reviews + negative_reviews)
word_index = tokenizer.word_index

# Sequencing
sequences = tokenizer.texts_to_sequences(positive_reviews + negative_reviews)
padded_sequences = pad_sequences(sequences, maxlen=10, padding='post', truncating='post')

# Build a simple neural network for text classification
model = keras.Sequential([
    keras.layers.Embedding(input_dim=len(word_index) + 1, output_dim=16, input_length=10),
    keras.layers.Flatten(),
    keras.layers.Dense(24, activation='relu'),
    keras.layers.Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Training the model
model.fit(padded_sequences, labels, epochs=10)

# Make predictions
test_reviews = ["This movie is amazing!", "I couldn't enjoy this film."]
test_sequences = tokenizer.texts_to_sequences(test_reviews)
test_padded_sequences = pad_sequences(test_sequences, maxlen=10, padding='post', truncating='post')
predictions = model.predict(test_padded_sequences)

for i, review in enumerate(test_reviews):
    sentiment = "positive" if predictions[i] > 0.5 else "negative"
    print(f"Review: {review} | Sentiment: {sentiment} (Confidence: {predictions[i][0]:.2f})")
