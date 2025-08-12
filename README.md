# Hidden Markov Model – Würfelproblem (Viterbi-Dekodierung)

Dieses Programm implementiert ein **Hidden-Markov-Modell** (HMM) am Beispiel des klassischen Würfelproblems.  
Es unterstützt die **Viterbi-Dekodierung** sowohl in normaler als auch in logarithmischer Skala.  
Damit lassen sich Beobachtungssequenzen aus Würfelergebnissen analysieren und die wahrscheinlichste Abfolge von Zuständen (fairer oder gezinkter Würfel) bestimmen.

## Voraussetzungen
- Python 3.8 oder neuer
- Keine externen Bibliotheken erforderlich

## Ausführen des Programms
```bash
python main.py
```

## Bedienung über die Kommandozeile
Das Programm wird vollständig über **interaktive Eingaben** in der Kommandozeile bedient.

---

### 1. HMM erstellen
Wähle, ob das Standard-Würfelproblem aus der Vorlesung verwendet werden soll oder ob ein eigenes Hidden-Markov-Modell mit individuellen Zuständen, Startwahrscheinlichkeiten, Übergangswahrscheinlichkeiten und Emissionswahrscheinlichkeiten erstellt werden soll.

---
### 2. Beobachtungssequenz bereitstellen
Wähle, wie die Beobachtungssequenz erzeugt oder eingelesen werden soll:

- 'Datei einlesen' → Sequenz aus einer Datei im data/-Ordner laden.
- 'Zufällige Sequenz generieren' → Beobachtungssequenz mithilfe des zuvor definierten HMM zufällig erzeugen.
- 'Sequenz manuell eingeben' → Beobachtungssequenz manuell eingeben.

---
### 3. Dekodierungsmethode auswählen
Wähle, ob bei der Dekodierung normale oder logarithmische Wahrscheinlichkeiten verwendet werden sollen:

- 'Viterbi (normal)' → Direkte Wahrscheinlichkeiten (kann bei langen Sequenzen zu Underflow führen).
- 'Viterbi (logarithmisch)' → Stabilere Berechnung mit Logarithmen, um Underflow zu vermeiden.

---
### 4. Ergebnisse anzeigen
- Ausgabe der vorhergesagten Zustandsfolge.
- Falls die tatsächlichen Zustände bekannt sind, wird die Accuracy berechnet und angezeigt.

**Hinweis:**
Sollte während der Dekodierung folgender Fehler auftreten:
```bash
ValueError: Kein gültiger Pfad gefunden.
```
bedeutet dies, dass der Viterbi-Algorithmus keinen Pfad durch das Hidden-Markov-Modell mit positiver Wahrscheinlichkeit finden konnte, um die Zustandsfolge zu generieren.
Dies kann passieren, wenn es zu einem Underflow kommt und die Wahrscheinlichkeiten aller möglichen Pfade numerisch auf 0.0 fallen.

---
### 5. Reverse-Experiment
Wähle, ob die Beobachtungssequenz umgedreht werden soll, um den Viterbi-Pfad für die umgedrehte Sequenz neu zu berechnen.
Das Programm gibt anschließend den Vergleich zwischen dem Originalpfad und dem Reversepfad aus.
