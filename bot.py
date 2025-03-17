import random
import json
import difflib
from utils.web_scraper import get_live_scores  # Web Scraper importieren
from data import fragen_antworten  # Vorab definierte Fragen und Antworten

class SCBruckbergChatbot:
    def __init__(self):
        self.fragen_antworten = fragen_antworten
        self.feedback_speicher_datei = "feedback_daten.json"  # Speicherort für negatives Feedback

    def antworten(self, frage):
        frage = frage.lower()  # Frage in Kleinbuchstaben umwandeln

        # Wenn der Benutzer nach dem nächsten Gegner fragt
        if self._ist_frage_nach_naechstem_gegner(frage):
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
        antwort = self._finde_aehnliche_antwort(frage)
        if antwort:
            feedback, richtige_antwort = self.hole_feedback(antwort)
            if feedback == "nein":
                # Speichere negatives Feedback mit der richtigen Antwort
                self.speichere_negatives_feedback(frage, antwort, richtige_antwort)
            return antwort

        return "Tut mir leid, das weiß ich nicht. Frag mich etwas anderes!"

    def _ist_frage_nach_naechstem_gegner(self, frage):
        """Hilfsmethode, um zu überprüfen, ob die Frage nach dem nächsten Gegner fragt."""
        return "herrenmannschaft" in frage or "nächster gegner" in frage or ("gegner" in frage and "herren" in frage)

    def _finde_aehnliche_antwort(self, frage):
        """Versucht, die ähnlichste Antwort anhand der Frage zu finden."""
        # Versuche zuerst eine Übereinstimmung mit 95% Ähnlichkeit
        passende_antwort = self._finde_antwort_mit_hoher_aehnlichkeit(frage)
        
        if passende_antwort:
            return passende_antwort  # Gibt Antwort zurück, wenn eine hohe Ähnlichkeit gefunden wurde

        # Falls keine Übereinstimmung mit hoher Ähnlichkeit gefunden wurde, überprüfe mit 70% und Schlüsselwörtern
        return self._finde_antwort_mit_schluesselwoertern(frage)

    def _finde_antwort_mit_hoher_aehnlichkeit(self, frage):
        """Sucht nach einer Antwort mit einer hohen Ähnlichkeit (95% oder mehr)."""
        beste_ähnlichkeit = 0
        passende_antwort = None

        for key, antworten in self.fragen_antworten.items():
            # Berechne die Ähnlichkeit zwischen der Frage und der gespeicherten Frage
            aehnlichkeit = difflib.SequenceMatcher(None, frage, key.lower()).ratio()

            # Wenn die Ähnlichkeit größer als 95% ist, wähle diese Antwort
            if aehnlichkeit >= 0.95:  # Schwellenwert für die Ähnlichkeit
                beste_ähnlichkeit = aehnlichkeit
                if isinstance(antworten, list):
                    passende_antwort = random.choice(antworten)
                else:
                    passende_antwort = antworten
                return passende_antwort

        return None  # Keine hohe Übereinstimmung gefunden

    def _finde_antwort_mit_schluesselwoertern(self, frage):
        """Durchsucht die Antwort basierend auf Schlüsselwörtern bei einer Ähnlichkeit von über 70%."""
        beste_ähnlichkeit = 0
        passende_antwort = None

        for key, antworten in self.fragen_antworten.items():
            aehnlichkeit = difflib.SequenceMatcher(None, frage, key.lower()).ratio()
            if aehnlichkeit >= 0.7:  # Schwellenwert für die Ähnlichkeit
                # Überprüfe, ob Schlüsselwörter in der Frage enthalten sind
                if any(keyword in frage for keyword in key.split()):
                    beste_ähnlichkeit = aehnlichkeit
                    if isinstance(antworten, list):
                        passende_antwort = random.choice(antworten)
                    else:
                        passende_antwort = antworten
                    break

        return passende_antwort if beste_ähnlichkeit >= 0.7 else None

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
        feedback_daten = self.lade_feedback_daten()

        feedback_daten["feedback"].append({
            "frage": frage,
            "falsche_antwort": falsche_antwort,
            "richtige_antwort": richtige_antwort if richtige_antwort else "",  # Falls keine richtige Antwort eingegeben wurde, leere Zeichenkette speichern
            "korrekt": False
        })

        self.speichere_feedback_daten(feedback_daten)

    def lade_feedback_daten(self):
        """Lädt die Feedback-Daten aus der JSON-Datei und gibt sie zurück."""
        try:
            with open(self.feedback_speicher_datei, "r") as f:
                feedback_daten = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            feedback_daten = {"feedback": []}
        return feedback_daten

    def speichere_feedback_daten(self, feedback_daten):
        """Speichert Feedback-Daten in der JSON-Datei."""
        with open(self.feedback_speicher_datei, "w") as f:
            json.dump(feedback_daten, f, indent=4)

    def trainiere_model(self):
        """Trainiert das Modell mit den gesammelten Trainingsdaten und Feedback-Daten."""
        fragen_feedback, falsche_antworten_feedback, richtige_antworten_feedback = self.lade_feedback_daten_und_verarbeiten()

        print("Gesammelte Feedback-Daten zur Verbesserung des Modells:")
        for frage, falsche_antwort, richtige_antwort in zip(fragen_feedback, falsche_antworten_feedback, richtige_antworten_feedback):
            print(f"Frage: {frage}, Falsche Antwort: {falsche_antwort}, Richtige Antwort: {richtige_antwort}")

    def lade_feedback_daten_und_verarbeiten(self):
        """Lädt die Feedback-Daten aus der JSON-Datei, verarbeitet sie und gibt sie zurück."""
        feedback_daten = self.lade_feedback_daten()

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
    frage = "Wer ist der zweite Abteilungsleiter des fußballs?"
    print(bot.antworten(frage))  # Teste mit der genauen Frage
    frage = "Wer ist der zweite Abteilungsleiter?"  # Teste mit abweichender Frage
    print(bot.antworten(frage))
    bot.trainiere_model()
