from typing import Tuple, List

class FileParser:

    @staticmethod
    def parse_file(filepath: str) -> Tuple[List[str], List[str]]:
        try:
            # Datei öffnen und Zeilen einlesen
            # Strip entfernt \n und Leerzeichen, leere Zeilen werden ignoriert
            with open(filepath, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip()]
                
                # Datei muss mindestens 2 Zeilen enthalten (Zahlen + Zustände)
                if len(lines) < 2:
                    raise ValueError("Die Datei muss mindestens zwei Zeilen enthalten: Zahlenfolge und Zustände.")
                
                # Erste Zeile: Nur den Teil nach dem Doppelpunkt nehmen (falls vorhanden)
                zahlenfolge = lines[0].split(':')[-1].strip()
                # In einzelne Zeichen (Zahlen) aufsplitten
                observations = list(zahlenfolge)

                # Zweite Zeile: Zustandsfolge extrahieren
                zustandsfolge = lines[1].split(':')[-1].strip()
                # In einzelne Zeichen (Zustände) aufsplitten
                states = list(zustandsfolge)

                # Sicherstellen, dass beide Folgen gleich lang sind
                if len(observations) != len(states):
                    raise ValueError("Zahlenfolge und Zustandsfolge haben unterschiedliche Längen.")

                # Beobachtungen und Zustände als Tupel zurückgeben
                return observations, states

        except FileNotFoundError:
            # Falls die Datei nicht existiert
            raise FileNotFoundError(f"Datei '{filepath}' nicht gefunden.")
        except Exception as e:
            # Allgemeiner Fehler beim Parsen
            raise IOError(f"Fehler beim Parsen der Datei '{filepath}': {e}")
