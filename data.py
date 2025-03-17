import json

# Beispiel-Daten für Training mit Frage-Antwort-Zuordnung
fragen_antworten = {
    "wer ist der beste spieler": "Christian Kranz ist der beste Spieler.",
    "wie viele teams hat der verein": "Im Jahr 2025 hat der Verein aktuell 15 Teams.",
    "wann wurde der verein gegründet": "Der Verein wurde 1946 gegründet.",
    "wie heißt das stadion des sc bruckberg": "Der SC Bruckberg spielt auf dem Sportgelände Bruckberg an der Dammstraße 12, 84079 Bruckberg.",
    "welche farben hat der sc bruckberg": "Die Vereinsfarben sind Blau und Weiß.",
    "wo liegt der sc bruckberg": "Der SC Bruckberg ist ein Fußballverein aus Bruckberg, Bayern.",
    "wie lautet die adresse des sc bruckberg": "Die Vereinsadresse lautet: Dammstr. 12, 84079 Bruckberg.",
    "hat der sc bruckberg eine website": "Ja, die Webseite des SC Bruckberg ist http://www.sc-bruckberg.de.",
    "welche mannschaften hat der sc bruckberg": "Der SC Bruckberg stellt folgende Mannschaften: Herren, Herren-Reserve, A-Junioren, C-Junioren, D-Junioren, E-Junioren I und II, F-Junioren 1 (2 Teams), F-Junioren 2 (2 Teams) und Frauen.",
    "in welchem bezirk spielt der sc bruckberg": "Der SC Bruckberg gehört zum Bezirk Niederbayern.",
    "in welchem kreis spielt der sc bruckberg": "Der SC Bruckberg spielt im Kreis Niederbayern West.",
 }

# Feedback-Daten aus der JSON-Datei laden
def lade_feedback():
    try:
        with open("feedback_daten.json", "r") as file:
            feedback_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        feedback_data = {"feedback": []}
    
    return feedback_data

# Kombiniere statische Fragen mit Feedback-Daten
def kombiniere_daten():
    feedback_data = lade_feedback()
    
    for feedback in feedback_data["feedback"]:
        if "frage" in feedback and "richtige_antwort" in feedback:
            fragen_antworten[feedback["frage"]] = feedback["richtige_antwort"]

# Vor dem Start des Bots Feedback-Daten einbinden
kombiniere_daten()
