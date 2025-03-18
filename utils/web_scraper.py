import requests
from bs4 import BeautifulSoup

def get_live_scores():
    # URL der SC Bruckberg Seite
    url = "https://www.bfv.de/vereine/sc-bruckberg/00ES8GNHVS00000AVV0AG08LVUPGND5I"
    
    try:
        # Anfrage an die Webseite senden
        response = requests.get(url)
        response.raise_for_status()  # Fehler auslösen, falls die Anfrage fehlschlägt
        
        # HTML-Inhalt der Seite parsen
        soup = BeautifulSoup(response.text, "html.parser")

        # Gegner-Teamname extrahieren
        gegner = soup.select_one("div.bfv-matchdata-result__team-name--team0")
        gegner_name = gegner.text.strip() if gegner else "Unbekannt"

        # Datum & Uhrzeit extrahieren
        datum_uhrzeit = soup.select_one(
            "div.bfv-spieltag-eintrag:nth-child(3) > div:nth-child(1) > a:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > span:nth-child(2)"
        )
        spiel_datum_uhrzeit = datum_uhrzeit.text.strip() if datum_uhrzeit else "Datum/Uhrzeit unbekannt"

        # Spielort extrahieren
        spielort = soup.select_one("div.bfv-spieltag-eintrag:nth-child(3) > div:nth-child(1) > div:nth-child(4)")
        if spielort:
            spiel_ort = spielort.text.strip()
        else:
            spiel_ort = "⚠️ Der Spielort ist derzeit nicht verfügbar."

        # Finale Ausgabe formatieren
        return (
            f"📅 Datum & Uhrzeit: {spiel_datum_uhrzeit}\n"
            f"⚽ Nächster Gegner: {gegner_name}\n"
            f"📍 Spielort: {spiel_ort}"
        )
    
    except requests.RequestException as e:
        # Fehler bei der HTTP-Anfrage
        return f"❌ Fehler bei der Anfrage: {e}"

# Beispielaufruf:
if __name__ == "__main__":
    print(get_live_scores())
