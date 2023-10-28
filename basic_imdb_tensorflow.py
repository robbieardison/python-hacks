import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Load the IMDb dataset
imdb = tf.keras.datasets.imdb
(train_data, train_labels), (test_data, test_labels) = imdb.load_data(num_words=10000)

# Load the word index (for decoding reviews)
word_index = imdb.get_word_index()

# Reverse the word index to decode reviews
reverse_word_index = dict([(value, key) for (key, value) in word_index.items()])

# Decode a review
def decode_review(text):
    return ' '.join([reverse_word_index.get(i, '?') for i in text])

# Padding the sequences
train_data = pad_sequences(train_data, maxlen=250, padding='post', truncating='post')
test_data = pad_sequences(test_data, maxlen=250, padding='post', truncating='post')

# Build a simple neural network for text classification
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(input_dim=10000, output_dim=16, input_length=250),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(24, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Training the model
model.fit(train_data, train_labels, epochs=10)

# Make predictions
test_reviews = ["This movie is amazing!", "I couldn't enjoy this film."]
test_sequences = [[word_index.get(word, 2) for word in review.split()] for review in test_reviews]
test_data = pad_sequences(test_sequences, maxlen=250, padding='post', truncating='post')
predictions = model.predict(test_data)

for i, review in enumerate(test_reviews):
    sentiment = "positive" if predictions[i] > 0.5 else "negative"
    print(f"Review: {review} | Sentiment: {sentiment} (Confidence: {predictions[i][0]:.2f})")
