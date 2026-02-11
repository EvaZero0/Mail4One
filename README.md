# Mail4One - Thunderbird Unsubscribe Tool

Mail4One ist ein Python-Tool, das deine lokalen Thunderbird-Profile nach Newslettern und Mailinglisten durchsucht. Es hilft dir, den Überblick über deine E-Mail-Abonnements zu behalten und dich einfach von unerwünschten Verteilern abzumelden.

## Funktionen

*   **Automatische Erkennung:** Findet automatisch dein Thunderbird-Profil unter Windows.
*   **Intelligenter Scan:** Durchsucht relevante Ordner (Inbox, Newsletter, Subscriptions, Mailing Lists) in lokalen und IMAP-Konten.
*   **Sicherheit:** Extrahiert "List-Unsubscribe"-Links und prüft dabei, ob die Domain des Links zum Absender passt (Phishing-Schutz).
*   **Benutzeroberfläche:** Übersichtliche GUI (Tkinter), die Absender nach Häufigkeit sortiert anzeigt.
*   **One-Click-Unsubscribe:** Öffnet den Abmeldelink direkt in deinem Standard-Browser.

## Installation

1.  Klone das Repository:
    ```bash
    git clone https://github.com/EvaZero0/Mail4One.git
    cd Mail4One
    ```

2.  Installiere die Abhängigkeiten:
    ```bash
    pip install -r requirements.txt
    ```

## Nutzung

Starte das Programm über die Kommandozeile:

```bash
python src/main.py
```

Das Tool beginnt sofort mit der Analyse und öffnet anschließend ein Fenster mit den Ergebnissen.

## Anforderungen

*   Python 3.x
*   Mozilla Thunderbird (installiert und eingerichtet)
*   Windows (aufgrund der Pfad-Struktur für AppData)

## Entwicklung

Der Code befindet sich im `src`-Ordner:
*   `main.py`: Einstiegspunkt der Anwendung.
*   `analyzer.py`: Logik zum Scannen der Mbox-Dateien und Extrahieren der Links.
*   `gui.py`: Benutzeroberfläche mit Tkinter.
