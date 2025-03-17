import random
import json
from utils.web_scraper import get_live_scores  # Web Scraper importieren
from data import fragen_antworten  # Vorab definierte Fragen und Antworten

class SCBruckbergChatbot:
    def __init__(self):
        self.fragen_antworten = fragen_antworten
        self.feedback_speicher_datei = "feedback_daten.json"  # Speicherort für negatives Feedback

    def antworten(self, frage):
        frage = frage.lower()  # Frage in Kleinbuchstaben umwandeln

        # Wenn der Benutzer nach dem nächsten Gegner fragt
        if "herrenmannschaft" in frage or "nächster gegner" in frage or ("gegner" in frage and "herren" in frage):
            naechsterGegnerHerrenmannschaft = get_live_scores()  # Web Scraper verwenden
            if naechsterGegnerHerrenmannschaft:
                # Frage den Benutzer nach Feedback
                feedback, richtige_antwort = self.hole_feedback(naechsterGegnerHerrenmannschaft)
                if feedback == "nein":
                    # Speichere negatives Feedback mit der richtigen Antwort
                    self.speichere_negatives_feedback(frage, naechsterGegnerHerrenmannschaft, richtige_antwort)
                return naechsterGegnerHerrenmannschaft
            else:
                return "Leider konnte ich den Spielplan nicht finden."

        # Vorab definierte Fragen und Antworten (mit random Auswahl)
        for key in self.fragen_antworten:
            if key in frage:
                antwort = random.choice(self.fragen_antworten[key])  # Zufällige Antwort aus mehreren Möglichkeiten
                # Frage den Benutzer nach Feedback
                feedback, richtige_antwort = self.hole_feedback(antwort)
                if feedback == "nein":
                    # Speichere negatives Feedback mit der richtigen Antwort
                    self.speichere_negatives_feedback(frage, antwort, richtige_antwort)
                return antwort

        return "Tut mir leid, das weiß ich nicht. Frag mich etwas anderes!"

    def hole_feedback(self, antwort):
        """Fragt den Benutzer nach Feedback zur Antwort und ermöglicht eine Korrektur."""
        print(f"Bot: War meine Antwort '{antwort}' korrekt? (ja/nein)")

        feedback = input("Bitte geben Sie 'ja' oder 'nein' ein: ").lower()
        while feedback not in ['ja', 'nein']:
            print("Bitte geben Sie 'ja' oder 'nein' ein.")
            feedback = input("War meine Antwort korrekt? (ja/nein): ").lower()

        richtige_antwort = None
        if feedback == "nein":
            richtige_antwort = input("Was wäre die richtige Antwort? ")

        return feedback, richtige_antwort

    def speichere_negatives_feedback(self, frage, falsche_antwort, richtige_antwort):
        """Speichert das negative Feedback (falsche Antworten) und die richtige Antwort für spätere Verbesserung."""
        try:
            with open(self.feedback_speicher_datei, "r") as f:
                feedback_daten = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            feedback_daten = {"feedback": []}

        if "feedback" not in feedback_daten:
            feedback_daten["feedback"] = []

        feedback_daten["feedback"].append({
            "frage": frage,
            "falsche_antwort": falsche_antwort,
            "richtige_antwort": richtige_antwort if richtige_antwort else "",  # Falls keine richtige Antwort eingegeben wurde, leere Zeichenkette speichern
            "korrekt": False
        })

        with open(self.feedback_speicher_datei, "w") as f:
            json.dump(feedback_daten, f, indent=4)

    def trainiere_model(self):
        """Trainiert das Modell mit den gesammelten Trainingsdaten und Feedback-Daten."""
        fragen_feedback, falsche_antworten_feedback, richtige_antworten_feedback = self.lade_feedback_daten()

        print("Gesammelte Feedback-Daten zur Verbesserung des Modells:")
        for frage, falsche_antwort, richtige_antwort in zip(fragen_feedback, falsche_antworten_feedback, richtige_antworten_feedback):
            print(f"Frage: {frage}, Falsche Antwort: {falsche_antwort}, Richtige Antwort: {richtige_antwort}")

    def lade_feedback_daten(self):
        """Lädt die Feedback-Daten aus der JSON-Datei und gibt sie zurück."""
        try:
            with open(self.feedback_speicher_datei, "r") as f:
                feedback_daten = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            feedback_daten = {"feedback": []}

        fragen_feedback = []
        falsche_antworten_feedback = []
        richtige_antworten_feedback = []

        for feedback in feedback_daten.get("feedback", []):
            fragen_feedback.append(feedback.get("frage", ""))
            falsche_antworten_feedback.append(feedback.get("falsche_antwort", ""))
            richtige_antworten_feedback.append(feedback.get("richtige_antwort", ""))

        return fragen_feedback, falsche_antworten_feedback, richtige_antworten_feedback


if __name__ == "__main__":
    bot = SCBruckbergChatbot()
    frage = "Wann ist das nächste Spiel der Herrenmannschaft?"
    print(bot.antworten(frage))
    bot.trainiere_model()
