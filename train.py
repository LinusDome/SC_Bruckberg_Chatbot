import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Beispiel-Daten für Training
fragen = ["wann ist das nächste spiel?", "wo finde ich tickets?", "wer hat das letzte spiel gewonnen?", "wer sind die besten spieler?"]
antworten = ["spiel", "tickets", "spielstand", "spieler"]

# Vektorisierung (Text in Zahlen umwandeln)
vectorizer = CountVectorizer()
X_train = vectorizer.fit_transform(fragen)

# Modell trainieren
model = MultinomialNB()
model.fit(X_train, antworten)

# Modell speichern
with open("models/chatbot_model.pkl", "wb") as f:
    pickle.dump((vectorizer, model), f)