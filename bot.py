import random
from utils.web_scraper import get_live_scores  # Web Scraper importieren
from data import fragen_antworten  # Vorab definierte Fragen und Antworten

class SCBruckbergChatbot:
    def __init__(self):
        self.fragen_antworten = fragen_antworten

    def antworten(self, frage):
        frage = frage.lower()  # Frage in Kleinbuchstaben umwandeln

        # Wenn der Benutzer nach dem Spielplan oder dem nächsten Gegner fragt
        if "spielplan" in frage or "nächster gegner" in frage or ("gegner" in frage and "herren" in frage):
            spiele = get_live_scores()  # Web Scraper verwenden
            if spiele:
                return spiele  # Einfach den Text zurückgeben, ohne .join()
            else:
                return "Leider konnte ich den Spielplan nicht finden."

        # Vorab definierte Fragen und Antworten (mit random Auswahl)
        for key in self.fragen_antworten:
            if key in frage:
                return random.choice(self.fragen_antworten[key])  # Zufällige Antwort aus mehreren Möglichkeiten

        return "Tut mir leid, das weiß ich nicht. Frag mich etwas anderes!"