import json

# Beispiel-Daten für Training
fragen = [
    "Wer ist der beste Spieler?",
    "Wie viele Teams hat der Verein?",
    "Wann wurde der Verein gegründet?",
]

antworten = [
    "Christian Kranz ist der beste Spieler.",
    "Im Jahr 2025 hat der Verein aktuell 15 Teams.",
    "Der Verein wurde 1946 gegründet.",
]

# Feedback-Daten aus der JSON-Datei laden
def lade_feedback():
    try:
        with open("feedback_daten.json", "r") as file:
            feedback_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        feedback_data = []
    
    return feedback_data

# Kombiniere die Daten aus data.py und die Feedback-Daten
def kombiniere_daten():
    feedback_data = lade_feedback()
    
    # Annahme: feedback_data enthält "frage" und "korrekt" (ob die Antwort korrekt war)
    fragen_feedback = [feedback["frage"] for feedback in feedback_data if feedback.get("korrekt", False)]
    antworten_feedback = ["Feedback-Antwort" for _ in fragen_feedback]  # Setze eine allgemeine Antwort, basierend auf dem Feedback
    
    # Kombiniere die bestehenden Fragen und Feedback-Daten
    combined_fragen = fragen + fragen_feedback
    combined_antworten = antworten + antworten_feedback
    
    return combined_fragen, combined_antworten

# Definiere hier die Variablen, die später importiert werden
fragen_antworten = {
    "fragen": fragen,
    "antworten": antworten
}
