import random
import json
from utils.web_scraper import get_live_scores  # Web Scraper importieren
from data import fragen_antworten  # Vorab definierte Fragen und Antworten

class SCBruckbergChatbot:
    def __init__(self):
        self.fragen_antworten = fragen_antworten
        self.feedback_speicher_datei = "feedback_daten.json"  # Speicherort für Feedback-Daten
        self.lade_feedback_daten()  # Feedback-Daten beim Start laden

    def lade_feedback_daten(self):
        """Lädt die Feedback-Daten aus der JSON-Datei und integriert sie in die bekannten Antworten."""
        try:
            with open(self.feedback_speicher_datei, "r") as f:
                feedback_daten = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            feedback_daten = {"feedback": []}

        for feedback in feedback_daten.get("feedback", []):
            frage = feedback.get("frage", "").lower()
            richtige_antwort = feedback.get("richtige_antwort", "")

            if frage and richtige_antwort:
                self.fragen_antworten[frage] = [richtige_antwort]

    def antworten(self, frage):
        frage = frage.lower().strip()  # Normalisierung der Frage

        # Live-Daten für die Herrenmannschaft abrufen
        if "herrenmannschaft" in frage or "nächster gegner" in frage or ("gegner" in frage and "herren" in frage):
            naechster_gegner = get_live_scores()
            if naechster_gegner:
                return self.feedback_prozess(frage, naechster_gegner)
            return "Leider konnte ich den Spielplan nicht finden."

        # Standardantworten durchsuchen
        for key in self.fragen_antworten:
            if key in frage:
                antwort = random.choice(self.fragen_antworten[key])
                return self.feedback_prozess(frage, antwort)

        return "Tut mir leid, das weiß ich nicht. Frag mich etwas anderes!"

    def feedback_prozess(self, frage, antwort):
        """Fragt den Benutzer nach Feedback zur Antwort und speichert Korrekturen."""
        print(f"Bot: War meine Antwort '{antwort}' korrekt? (ja/nein)")

        feedback = input("Bitte geben Sie 'ja' oder 'nein' ein: ").lower()
        while feedback not in ['ja', 'nein']:
            feedback = input("Bitte geben Sie 'ja' oder 'nein' ein: ").lower()

        if feedback == "nein":
            richtige_antwort = input("Was wäre die richtige Antwort? ").strip()
            self.speichere_negatives_feedback(frage, antwort, richtige_antwort)
            return f"Danke für dein Feedback! Ich habe gelernt, dass die richtige Antwort '{richtige_antwort}' ist."

        return antwort

    def speichere_negatives_feedback(self, frage, falsche_antwort, richtige_antwort):
        """Speichert das Feedback und verbessert die Antworten für zukünftige Anfragen."""
        try:
            with open(self.feedback_speicher_datei, "r") as f:
                feedback_daten = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            feedback_daten = {"feedback": []}

        # Sicherstellen, dass das Feedback-Datenfeld existiert
        if "feedback" not in feedback_daten:
            feedback_daten["feedback"] = []

        # Feedback speichern
        feedback_daten["feedback"].append({
            "frage": frage,
            "falsche_antwort": falsche_antwort,
            "richtige_antwort": richtige_antwort
        })

        # Speichern in JSON-Datei
        with open(self.feedback_speicher_datei, "w") as f:
            json.dump(feedback_daten, f, indent=4)

        # Aktualisieren des internen Speichers
        self.fragen_antworten[frage] = [richtige_antwort]

    def trainiere_model(self):
        """Zeigt die gespeicherten Feedback-Daten an."""
        try:
            with open(self.feedback_speicher_datei, "r") as f:
                feedback_daten = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            feedback_daten = {"feedback": []}

        print("Gesammelte Feedback-Daten zur Verbesserung des Modells:")
        for feedback in feedback_daten.get("feedback", []):
            print(f"Frage: {feedback['frage']}, Korrektur: {feedback['richtige_antwort']}")

if __name__ == "__main__":
    bot = SCBruckbergChatbot()
    print("⚽ Willkommen beim SC Bruckberg Chatbot! Frag mich etwas über den Verein. (Tippe 'exit' zum Beenden)")

    while True:
        user_input = input("Du: ").strip().lower()
        if user_input == "exit":
            print("Bot: Bis bald!")
            break
        print(f"Bot: {bot.antworten(user_input)}")
