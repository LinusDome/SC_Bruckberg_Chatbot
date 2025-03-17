from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import pickle
from data import kombiniere_daten  # Importiere die Funktion zum Kombinieren der Daten

# Kombiniere die Daten aus data.py und feedback_daten.json
fragen, antworten = kombiniere_daten()

# Aufteilen der Daten in Trainings- und Testdaten (80% Training, 20% Test)
X_train, X_test, y_train, y_test = train_test_split(fragen, antworten, test_size=0.2, random_state=42)

# Vektorisierung der Fragen (Umwandlung von Text in Zahlen) mit TfidfVectorizer
vectorizer = TfidfVectorizer(stop_words='german', max_features=5000)  # Stopwords entfernen und max. Features setzen
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Trainiere das Modell (Multinomial Naive Bayes)
model = MultinomialNB()
model.fit(X_train_tfidf, y_train)

# Vorhersagen auf dem Testdatensatz
y_pred = model.predict(X_test_tfidf)

# Berechne die Genauigkeit und das Klassifizierungsreport
accuracy = accuracy_score(y_test, y_pred)
print(f"Modellgenauigkeit: {accuracy * 100:.2f}%")

# Klassifizierungsbericht ausgeben
print("Klassifizierungsbericht:")
print(classification_report(y_test, y_pred))

# Speichern des Modells und des Vektorisierers
with open("models/chatbot_model.pkl", "wb") as f:
    pickle.dump((vectorizer, model), f)
