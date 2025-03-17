import requests
from bs4 import BeautifulSoup

def get_live_scores():
    # URL der SC Bruckberg Seite
    url = "https://www.bfv.de/vereine/sc-bruckberg/00ES8GNHVS00000AVV0AG08LVUPGND5I"
    
    try:
        # Anfrage an die Webseite senden
        response = requests.get(url)
        response.raise_for_status()  # wirft eine Ausnahme, wenn der Statuscode nicht 200 ist
        
        # HTML-Inhalt der Seite parsen
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Suche nach dem nächsten Spiel anhand eines allgemeineren CSS-Selectors
        gegner = soup.select_one(
            "div.bfv-matchdata-result__team-name--team0"  # Der Selektor für den Namen des Gegners
        )
        
        # Wenn der Gegner gefunden wurde, gib ihn zurück
        if gegner:
            return f"Nächster Gegner: {gegner.text.strip()}"
        
        return "Kein Gegner gefunden oder der Spielplan konnte nicht korrekt abgerufen werden."
    
    except requests.RequestException as e:
        # Fehler bei der HTTP-Anfrage
        return f"Fehler bei der Anfrage: {e}"

# Beispielaufruf:
if __name__ == "__main__":
    print(get_live_scores())
