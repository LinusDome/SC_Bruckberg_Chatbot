from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle
from data import kombiniere_daten  # Importiere die Funktion zum Kombinieren der Daten

# Kombiniere die Daten aus data.py und feedback_daten.json
fragen, antworten = kombiniere_daten()

# Vektorisierung der Fragen (Umwandlung von Text in Zahlen)
vectorizer = CountVectorizer()
X_train = vectorizer.fit_transform(fragen)

# Trainiere das Modell (Multinomial Naive Bayes)
model = MultinomialNB()
model.fit(X_train, antworten)

# Speichern des Modells und des Vektorisierers
with open("models/chatbot_model.pkl", "wb") as f:
    pickle.dump((vectorizer, model), f)