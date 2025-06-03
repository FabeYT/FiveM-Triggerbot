
## FiveM Trigger Assistant – Ausführliche Programmbeschreibung

Der **FiveM Trigger Assistant** ist ein spezialisiertes Hilfsprogramm, entwickelt für Spieler von **FiveM**, einer beliebten Multiplayer-Modifikation für Grand Theft Auto V (GTA V). Dieses Tool dient als sogenannter **Trigger-Bot**, der automatisiert Mausklicks auslöst, wenn bestimmte visuelle Bedingungen auf dem Bildschirm erfüllt sind – was insbesondere in schnellen Spielsituationen einen strategischen Vorteil bieten kann.

### Zweck und Funktion

Der Kern des Programms besteht darin, die Farbe eines einzelnen Pixels im Zentrum des Bildschirms kontinuierlich zu überwachen. Basierend auf der erkannten Farbe wird eine automatisierte Reaktion ausgelöst:

* **Weißer Pixel als Startsignal:** Erkennt das Programm, dass der zentrale Pixel weiß ist, aktiviert es einen sogenannten **Trigger-Modus**. Dieser Modus signalisiert, dass das Programm nun bereit ist, auf eine weitere Bedingung zu reagieren.
* **Roter Pixel als Auslöser:** Innerhalb dieses Trigger-Modus wartet der Bot auf das Erscheinen eines roten Pixels an genau derselben Stelle. Sobald dieser erkannt wird, simuliert das Programm einen **linken Mausklick**.
* **Timeout-Mechanismus:** Um unbeabsichtigte oder endlose Triggerzustände zu vermeiden, wird der Trigger-Modus automatisch nach 20 Sekunden zurückgesetzt, falls kein roter Pixel erkannt wird.

### Technische Details

* **Pixel-Farbabfrage:** Das Programm nutzt die `pyautogui`-Bibliothek, um Screenshots vom zentralen Pixelbereich des Bildschirms zu erstellen und dessen RGB-Farbwerte auszulesen.
* **Farberkennung:** Die Farberkennung ist in zwei Kategorien unterteilt:

  * **Weiß:** Ein Pixel gilt als weiß, wenn alle RGB-Werte mindestens 220 betragen.
  * **Rot:** Ein Pixel gilt als rot, wenn der Rotwert deutlich über 150 liegt, während Grün- und Blauwerte deutlich darunter liegen.
* **Maussteuerung:** Der Mausklick wird über die `pynput`-Bibliothek simuliert, die den linken Maustasten-Down- und Up-Befehl automatisch ausführt.
* **Benutzeroberfläche (GUI):** Die Oberfläche ist mit `tkinter` gestaltet und bietet:

  * Eine Farbvorschau des aktuell überwachten Pixels.
  * Eine Statusanzeige mit Textinfos über den aktuellen Zustand.
  * Buttons zum Starten/Stoppen der Überwachung und zum Verstecken/Anzeigen des Fensters.
  * Hotkeys (F1 zum Starten/Stoppen, F2 zum Verstecken/Anzeigen) für komfortable Steuerung ohne die GUI nutzen zu müssen.

### Anwendungsgebiet und Nutzen

Der FiveM Trigger Assistant richtet sich an Spieler, die in FiveM schnell auf visuelle Signale reagieren müssen, beispielsweise bei Schusswechseln, Alarmzuständen oder anderen farblich kodierten Spielmechaniken. Durch die Automatisierung des Mausklicks können Reaktionszeiten erheblich verkürzt und repetitive Handlungen vereinfacht werden.

### Hinweis

Dieses Tool ist als Assistenzprogramm gedacht und sollte verantwortungsbewusst genutzt werden. Die Nutzung automatisierter Programme in Multiplayer-Spielen kann gegen die Nutzungsbedingungen des Spiels oder Servers verstoßen und zu Sanktionen führen. Bitte informiere dich über die Regeln deines Servers, bevor du den Trigger Assistant einsetzt.

