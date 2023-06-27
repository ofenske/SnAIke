# SnAIke
Bei diesem Spiel handelt es sich um ein herkömmliches Snake-Spiel, welches zusätzlich um ein paar Elemente erweitert wurde.
Zunächst wird es eine kurze Einführung in das Repo geben, bevor auf das Spiel an sich und seine Regeln eingegangen wird. 


## Getting started

Um das Spiel lokal auf deinem Rechner auszuführen benötigst du zunächst folgende Sachen:
- [ ] Python3.10
- [ ] Pipenv

Um dieses Code-Repo dann bei dir zum Laufen zu bringen, musst du lediglich in diesen Ordner navigieren und folgenden 
Befehl ausführen: `pipenv install`.   
Damit erstellst du ein neues Virtualenv und installierst du alle notwendigen Python-Packages, welche im [Pipfile](Pipfile) spezifiziert sind.

Als Nächstes siehst du zwei verschiedene Dateien in Content-Root:
* [play.py](play.py): Datei, welche ausgeführt werden kann, um das Spiel manuell zu spielen.
* [my_bot.py](my_bot.py): Datei, welche einen Starter-Bot enthält.

Beide Dateien können ohne zusätzliche Kommandozeilen-Parameter ausgeführt werden. 
Wollen wir also z. B. den Bot starten, so können wir  direkt mit dem Befehl `python my_bot.py` tun.
Weitere Erläuterungen zum Aufbau der einzelnen Dateien und wie ihr mit der SnAIke-Spielengine interagieren könnt, 
sind in den einzelnen Dateien nachzulesen.

## Spielregeln
Das Basis-Regeln sind genauso wie in jedem anderem Snake-Spiel definiert:
1. Jede weiße Frucht gibt +10 Punkte. Isst die Schlange eine Frucht, so verlängert sie sich um ein Segment.
2. Die Schlange darf sich nicht in den eigenen Schwanz beißen, sonst stirbt sie.
3. Die Schlange darf nicht aus der Map herauslaufen, sonst stirbt sie.

Darüber hinaus gibt es bei dieser Variante noch ein paar Extra-Regeln:
* Rote Früchte:
  * Respawn: Mit jeder gegessenen weißen Frucht erscheint eine weitere rote Frucht.
  * Wirkung: Schlange stirbt/Game Over!
  * Besonderheit: Besitzt die Schlange Super-Segmente und isst eine rote Frucht, dann verschwindet die Hälfte der roten 
  Früchte von der Map und man bekommt -50 Punkte. Die Schlange verliert zusätzlich alle verbleibenden Super-Segmente.
* Blaue Früchte: 
  * Respawn: Mit jeder gegessenen weißen Frucht erscheint eine weitere blaue Frucht.
  * Wirkung: Schlange ist paralysiert und führt unkontrolliert bis zu drei Bewegungen aus!
  * Besonderheit: Besitzt die Schlange Super-Segmente und isst eine blaue Frucht, dann verschwinden alle blauen 
  Früchte von der Map und man bekommt -50 Punkte. Die Schlange verliert zusätzlich alle verbleibenden Super-Segmente.
* Gelbe Früchte: 
  * Respawn: Mit jeder fünften weißen Frucht erscheint einmalig eine gelbe Frucht die direkt im nächsten Zug verschwindet, sollte sie nicht vor einer weißen Frucht gegessen werden.
  * Wirkung: Schlange ist immun gegenüber blauen und roten Früchten. Die nächsten 3 weißen Früchte geben jeweils 50 Punkte.

Du siehst also das es sich hier um eine Snake-Erweiterung handelt! Verwende einfach den Befehl `python play.py` und 
probiere das Spiel zunächst selbst aus, falls du nicht alle Regeln verstanden haben solltest.

Wenn du mit der Entwicklung deines Bots anfangen möchtest, ist der Starter-Bot aus [my_bot.py](my_bot.py) der richtige Weg, um ein wenig was auzuprobieren.
Am Ende werden wir auswerten, welches Team mit ihrem Bot die meisten Punkte sammeln kann und somit zum Sieger gekrönt wird.

## Spiel-Mechanik
Am Anfang jedes Spiels muss zunächst die Spiel-Engine wie folgt initialisiert werden: `game = snk.Game('BotName')`.
Anschließend kann der Bot verschiedene Informationen über den Zustand der Welt (=Map) abrufen.
Diese kann er z. B. mit `game.map_status` von der Spiel-Engine erfragen. Die Map hat dabei mehrere Attribute:
* snake_position = Position vom Schlangen-Kopf
* snake_body = Position aller Teile des Schlangen-Körpers in Form von x,y-Werten
* snake_direction = Die Richtung in die sich die Schlange aktuell bewegt als String: UP|DOWN|RIGHT|LEFT
* yellow_segments = Spiegelt die Anzahl der durch die gelbe Frucht verliehenen zusätzlichen Leben wieder.
* blue_segments = Spiegelt die verbleibende Anzahl der durch die blaue Frucht hervorgerufenen unkontrollierbaren Bewegungen wieder.
* white_fruit = x,y-Koordinaten von der weißen Frucht als Liste: [x,y]
* yellow_fruit = x,y-Koordinaten von der gelben Frucht als Liste: [x,y]
* red_fruit = x,y-Koordinaten aller roten Früchte als Liste von Listen: [[x1,y1],...,[xn, yn]]
* blue_fruit = x,y-Koordinaten aller blauen Früchte als Liste von Listen: [[x1,y1],...,[xn, yn]]
* window_x = Maximale x-Koordinate 
* window_y = Maximale y-Koordinate

Auf Basis dieses Wissens kann der Bot dann für jeden Zug eine Aktion an die Spiel-Engine zurückmelden. Dabei kann er 
aus den folgenden Aktionen wählen:
* "UP": Bewege die Schlange nach oben.
* "DOWN": Bewege die Schlange nach unten.
* "RIGHT": Bewege die Schlange nach rechts
* "LEFT": Bewege die Schlange nach links.
* None: Tue gar nichts.

Mit dem Befehl `game.send_command("Aktionsname")` wird die jeweilige Aktion dann an die Spiel-Engine gesendet 
und der nächste Zu wird berechnet. Wie schon weiter oben beschrieben, ist in [my_bot.py](my_bot.py) ein Beispiel für 
einen einfachen Bot implementiert. Hier können sie weitere Informationen sammeln.