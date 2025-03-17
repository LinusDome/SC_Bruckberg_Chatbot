import requests
from bs4 import BeautifulSoup

def get_live_scores():
    url = "https://www.bfv.de/vereine/sc-bruckberg/00ES8GNHVS00000AVV0AG08LVUPGND5I"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    spiele = []
    for match in soup.find_all("div", class_="spiel"):
        datum = match.find("span", class_="datum").text
        gegner = match.find("span", class_="gegner").text
        ergebnis = match.find("span", class_="ergebnis").text
        spiele.append(f"{datum}: {gegner} - Ergebnis: {ergebnis}")

    return spiele

if __name__ == "__main__":
    print(get_live_scores())