# Projekt Luftzirkulation Steuerung

## Ausführung

In einem Terminal Emulator `./main.py` ausführen. Mit `Strg-C` können sie das Programm stoppen.

## Abhängigkeiten 

Liste on benötigten Libraries:

* RPi.GPIO 
* time(Builtin)
* datetime(Builtin)

Installation von Abhängigkeiten:

**Mit pip**

```
$ pip install RPi.GPIO paho.mqtt.client
```

oder

**Mit pipx**
```
$ pipx install RPi.GPIO paho.mqtt.client
```

oder

**Mit apt**
```
$ sudo apt install rpi.gpio
```
## Prozess

### Schritt 1: Skizze der geplanten Box

Um das Projekt zu beginnen, haben wir eine Skizze unserer geplanten Box erstellt. Diese Skizze diente als Grundlage für das Design und half uns dabei, die Platzierung der Komponenten sowie die Größe der Box zu bestimmen.

Die Skizze beinhaltet die Positionen für den Schrittmotor (welche später angepasst wurde) und den Temperatur/Feuchtigkeit-Sensor. Sie ermöglichte es uns, eine klare Vorstellung von der äußeren Erscheinung der Box zu erhalten und half bei der Planung des Zusammenbaus.

![Skizze-Dachluken-Steuerung](skizze-dachluken-steuerung.png)

### Schritt 2: Vorbereitung

Im Vorbereitungsprozess haben wir den Temperatur/Feuchtigkeit-Sensor, Eclipse-MQTT-Broker und den Schrittmotor einzeln getestet und zum Laufen gebracht. Dies wurde durch die Entwicklung separater Programmcodes für jeden Sensor erreicht. Hier sind die durchgeführten Tests:

Schrittmotor: 
* Es wurde Sample-Code verwendet um die funktion zu testen des Schrittmotors. 
* Ein Programm wurde erfasst um die funktion mit einem MQTT Subscription process zu verknüpfen. 

Temperatur/Feuchtigkeit-Sensor:
* Der Temperatur/Feuchtigkeit-Sensor wurde, mit hilfe offizieller Dokumentation und Sample-Code, ausgelesen.
* Ein Programm wurde erfasst um die funktion mit einem MQTT Publish process zu verknüpfen. 

Eclipse-MQTT-Broker
* Wir haben die logs in `/var/log/mosquitto.log` analysiert und ausgewertet. 
* Wir haben einen -PUB und MQTT-SUB nachgestellt.

### Schritt 3: Entwicklung des Hauptprogramms

Im Hauptprogramm 
