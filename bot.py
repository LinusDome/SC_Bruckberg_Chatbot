import random
import json
import difflib
import logging
import spacy
from difflib import get_close_matches
from utils.web_scraper import get_live_scores  # Web Scraper importieren
from data import fragen_antworten  # Vorab definierte Fragen und Antworten


class SCBruckbergChatbot:
    def __init__(self, fragen_antworten):
        self.nlp = spacy.load("de_core_news_md")
        self.fragen_antworten = fragen_antworten
        self.feedback_speicher_datei = "feedback_daten.json"

        # Logging konfigurieren
        logging.basicConfig(
            filename="chatlog.txt",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    def antworten(self, frage):
        frage = frage.lower().strip()
        logging.info(f"User: {frage}")

        if self._ist_frage_nach_naechstem_gegner(frage):
            return self._handle_naechster_gegner()

        antwort = self._finde_aehnliche_antwort(frage)
        if antwort:
            return self._handle_feedback(frage, antwort)

        antwort = "Tut mir leid, das weiß ich nicht. Frag mich etwas anderes!"
        logging.info(f"Bot: {antwort}")
        return antwort

    def _handle_naechster_gegner(self):
        # Web Scraper aufrufen, um die Spieldaten zu erhalten
        spiel_info = get_live_scores()

        # Falls `spiel_info` ein String ist, direkt zurückgeben
        if isinstance(spiel_info, str):
            return self._handle_feedback("Nächstes Spiel", spiel_info)

        # Falls `spiel_info` kein Dictionary ist, Fehler behandeln
        if not isinstance(spiel_info, dict):
            antwort = "Leider konnte ich den Spielplan nicht finden."
            logging.warning("Spielplan nicht gefunden.")
            return antwort

        # Extrahiere die relevanten Informationen
        gegner = spiel_info.get("gegner", "Unbekannt")
        datum = spiel_info.get("datum", "Datum unbekannt")
        uhrzeit = spiel_info.get("uhrzeit", "Uhrzeit unbekannt")
        ort = spiel_info.get("ort", "Spielort unbekannt")

        # Formatierte Antwort
        antwort = (
            f"\U0001F4E2 **Nächstes Spiel:**\n"
            f"\U0001F4C5 **Datum:** {datum}\n"
            f"⏰ **Uhrzeit:** {uhrzeit}\n"
            f"⚽ **Gegner:** {gegner}\n"
            f"📍 **Spielort:** {ort}"
        )

        return self._handle_feedback("Nächstes Spiel", antwort)
        return self._handle_feedback("Nächstes Spiel", antwort)

    def _handle_feedback(self, frage, antwort):
        print(f"Bot: War meine Antwort '{antwort}' korrekt? (ja/nein)")
        feedback = input("Bitte geben Sie 'ja' oder 'nein' ein: ").strip().lower()

        if feedback == "nein":
            richtige_antwort = input("Was wäre die richtige Antwort? ").strip()
            self.speichere_negatives_feedback(frage, antwort, richtige_antwort)
        else:
            logging.info(f"Bot: {antwort}")

        return antwort

    def _ist_frage_nach_naechstem_gegner(self, frage):
        return any(
            keyword in frage
            for keyword in ["herrenmannschaft", "nächster gegner", "gegner", "herren"]
        )

    def _finde_aehnliche_antwort(self, frage):
        beste_antwort = self._finde_antwort_mit_hoher_aehnlichkeit(frage)
        return beste_antwort if beste_antwort else self._finde_antwort_mit_schluesselwoertern(frage)

    def _finde_antwort_mit_hoher_aehnlichkeit(self, frage):
        for key, antworten in self.fragen_antworten.items():
            if difflib.SequenceMatcher(None, frage, key.lower()).ratio() >= 0.95:
                return random.choice(antworten) if isinstance(antworten, list) else antworten
        return None

    def _finde_antwort_mit_schluesselwoertern(self, frage):
        frage_doc = self.nlp(frage)
        beste_antwort = None
        beste_ähnlichkeit = 0.7  # Mindest-Schwelle

        for key, antworten in self.fragen_antworten.items():
            gespeicherte_doc = self.nlp(key.lower())
            aehnlichkeit = frage_doc.similarity(gespeicherte_doc)

            if aehnlichkeit > beste_ähnlichkeit:
                beste_ähnlichkeit = aehnlichkeit
                beste_antwort = (
                    random.choice(antworten) if isinstance(antworten, list) else antworten
                )

        if not beste_antwort:
            naechste_frage = get_close_matches(frage, self.fragen_antworten.keys(), n=1, cutoff=0.5)
            if naechste_frage:
                beste_antwort = self.fragen_antworten[naechste_frage[0]]

        return beste_antwort

    def speichere_negatives_feedback(self, frage, falsche_antwort, richtige_antwort):
        feedback_daten = self.lade_feedback_daten()

        feedback_daten["feedback"].append(
            {
                "frage": frage,
                "falsche_antwort": falsche_antwort,
                "richtige_antwort": richtige_antwort or "",
                "korrekt": False,
            }
        )

        self.speichere_feedback_daten(feedback_daten)

    def lade_feedback_daten(self):
        try:
            with open(self.feedback_speicher_datei, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"feedback": []}

    def speichere_feedback_daten(self, feedback_daten):
        try:
            with open(self.feedback_speicher_datei, "w") as f:
                json.dump(feedback_daten, f, indent=4)
        except Exception as e:
            logging.error(f"Fehler beim Speichern des Feedbacks: {e}")

    def trainiere_model(self):
        fragen_feedback, falsche_antworten, richtige_antworten = self.lade_feedback_daten_und_verarbeiten()

        print("Gesammelte Feedback-Daten zur Verbesserung des Modells:")
        for frage, falsche, richtige in zip(fragen_feedback, falsche_antworten, richtige_antworten):
            print(f"Frage: {frage}, Falsche Antwort: {falsche}, Richtige Antwort: {richtige}")

    def lade_feedback_daten_und_verarbeiten(self):
        feedback_daten = self.lade_feedback_daten()

        return (
            [f.get("frage", "") for f in feedback_daten.get("feedback", [])],
            [f.get("falsche_antwort", "") for f in feedback_daten.get("feedback", [])],
            [f.get("richtige_antwort", "") for f in feedback_daten.get("feedback", [])],
        )


if __name__ == "__main__":
    bot = SCBruckbergChatbot(fragen_antworten)

    while True:
        frage = input("Du: ").strip()
        if frage.lower() == "exit":
            break
        print("Bot:", bot.antworten(frage))
