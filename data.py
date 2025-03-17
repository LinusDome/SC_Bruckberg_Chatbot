import json
import logging

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
    "wer ist der der trainer der ersten mannschaft": "Der Trainer heißt Manfred Böhlert",
    "wer ist der der zweite trainer der ersten mannschaft": "Der Trainer heißt Markus Baumgartner",
    "wer ist der der trainer der zweiten mannschaft": "Der Trainer heißt Markus Baumgartner",
    "18/19 a-klasse landshut": "Im Jahr 2018/19 spielte die Mannschaft in der A-Klasse Landshut und belegte den 9. Platz.",
    "17/18 a-klasse hallertau": "Im Jahr 2017/18 spielte die Mannschaft in der A-Klasse Hallertau und belegte den 11. Platz.",
    "16/17 a-klasse landshut": "Im Jahr 2016/17 spielte die Mannschaft in der A-Klasse Landshut und belegte den 9. Platz.",
    "15/16 a-klasse hallertau": "Im Jahr 2015/16 spielte die Mannschaft in der A-Klasse Hallertau und belegte den 4. Platz.",
    "14/15 a-klasse landshut": "Im Jahr 2014/15 spielte die Mannschaft in der A-Klasse Landshut und belegte den 7. Platz.",
    "13/14 a-klasse landshut": "Im Jahr 2013/14 spielte die Mannschaft in der A-Klasse Landshut und belegte den 9. Platz.",
    "12/13 kreisklasse landshut": "Im Jahr 2012/13 spielte die Mannschaft in der Kreisklasse Landshut und belegte den 12. Platz.",
    "11/12 kreisklasse landshut": "Im Jahr 2011/12 spielte die Mannschaft in der Kreisklasse Landshut und belegte den 7. Platz.",
    "10/11 kreisklasse landshut": "Im Jahr 2010/11 spielte die Mannschaft in der Kreisklasse Landshut und belegte den 10. Platz.",
    "09/10 a-klasse landshut": "Im Jahr 2009/10 spielte die Mannschaft in der A-Klasse Landshut und belegte den 1. Platz.",
    "03/04 bezirksliga west": "Im Jahr 2003/04 spielte die Mannschaft in der Bezirksliga West und belegte den 15. Platz.",
    "01/02 kreisliga landshut": "Im Jahr 2001/02 spielte die Mannschaft in der Kreisliga Landshut und belegte den 3. Platz.",
    "wer ist der erste abteilungsleiter des fußballs?": "Dies ist Michael Bauer mit dem Spitznamen GÜ.",
    "wer ist der zweite abteilungsleiter des fußballs?": "Dies ist Stefan Ackstaler mit dem Spitznamen ACKSE.",
    "wer ist der dritte abteilungsleiter des fußballs?": "Dies ist Markus Stadler mit dem Spitznamen Schneck.",
    "wie erreiche ich den fußball des sc bruckberg": "Über die Email: fußball@scbruckberg.de.",
    "24/25 a-klasse landshut": "Im Jahr 2024/25 spielte die Mannschaft in der A-Klasse Landshut und belegte den 8. Platz.",
    "23/24 a-klasse landshut": "Im Jahr 2023/24 spielte die Mannschaft in der A-Klasse Landshut und belegte den 3. Platz.",
    "22/23 a-klasse mainburg": "Im Jahr 2022/23 spielte die Mannschaft in der A-Klasse Mainburg und belegte den 3. Platz.",
    "21/22 a-klasse landshut": "Im Jahr 2021/22 spielte die Mannschaft in der A-Klasse Landshut und belegte den 2. Platz.",
    "19/21 a-klasse landshut": "Im Jahr 2019/21 spielte die Mannschaft in der A-Klasse Landshut und belegte den 8. Platz."
}

# Logging konfigurieren
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Feedback-Daten aus der JSON-Datei laden
def lade_feedback():
    try:
        with open("feedback_daten.json", "r") as file:
            feedback_data = json.load(file)
        logging.info("Feedback-Daten erfolgreich geladen.")
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Fehler beim Laden der Feedback-Daten: {e}")
        feedback_data = {"feedback": []}
    
    return feedback_data

# Kombiniere statische Fragen mit Feedback-Daten
def kombiniere_daten():
    feedback_data = lade_feedback()
    
    # Sicherstellen, dass keine Frage überschrieben wird, falls sie bereits vorhanden ist
    for feedback in feedback_data["feedback"]:
        frage = feedback.get("frage")
        richtige_antwort = feedback.get("richtige_antwort")
        
        if frage and richtige_antwort:
            if frage not in fragen_antworten:
                fragen_antworten[frage] = richtige_antwort
                logging.info(f"Neue Frage-Antwort-Paar hinzugefügt: {frage}")
            else:
                logging.warning(f"Frage bereits vorhanden, überspringe: {frage}")

# Vor dem Start des Bots Feedback-Daten einbinden
kombiniere_daten()
