import os
from src.hidden_markov_model import HMM
from src.viterbi_decoder import ViterbiDecoder
from src.sequence_generator import SequenceGenerator
from src.file_parser import FileParser

# =============================
# Hilfsfunktionen für Nutzereingaben
# =============================

def ask_choice(prompt: str, options: list[str]) -> str:
    """Fragt den Benutzer nach einer Auswahl aus einer Liste von Optionen."""
    print(f"\n{prompt}")
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")

    while True:
        try:
            choice = int(input("Deine Wahl (Zahl eingeben): "))
            if 1 <= choice <= len(options):
                return options[choice - 1]
            else:
                print(f"Bitte gib eine Zahl zwischen 1 und {len(options)} ein.")
        except ValueError:
            print("Ungültige Eingabe. Bitte eine Zahl eingeben.")

def ask_int(prompt: str, min_val: int = None, max_val: int = None) -> int:
    """Fragt eine Ganzzahl ab (optional mit Min-/Max-Bereich)."""
    while True:
        try:
            value = int(input(f"{prompt}: ").strip())
            if (min_val is not None and value < min_val) or (max_val is not None and value > max_val):
                print("[ERROR] Zahl außerhalb des gültigen Bereichs.")
                continue
            return value
        except ValueError:
            print("[ERROR] Bitte eine gültige Ganzzahl eingeben.")

def ask_float(prompt: str, min_val: float = 0.0, max_val: float = 1.0) -> float:
    """Fragt eine Fließkommazahl ab, z. B. für Wahrscheinlichkeiten."""
    while True:
        try:
            value = float(input(f"{prompt}: ").strip())
            if value < min_val or value > max_val:
                print(f"[ERROR] Wert muss zwischen {min_val} und {max_val} liegen.")
                continue
            return value
        except ValueError:
            print("[ERROR] Bitte eine gültige Kommazahl eingeben.")

def ask_yes_no(prompt: str) -> bool:
    """Ja/Nein-Abfrage (y/n)."""
    while True:
        value = input(f"{prompt} (y/n): ").strip().lower()
        if value in ("y", "yes"):
            return True
        elif value in ("n", "no"):
            return False
        print("[ERROR] Bitte 'y' oder 'n' eingeben.")

# =============================
# HMM-Konfiguration
# =============================

def ask_hmm() -> HMM:
    """Fragt den Benutzer, ob er ein fertiges HMM laden oder manuell erstellen möchte."""
    print("\n=== HMM-Konfiguration ===")
    choice = ask_choice("Wie möchten Sie das HMM erstellen?", ["Würfelproblem (vordefiniert)", "Selbst eingeben"])

    if choice == "Würfelproblem (vordefiniert)":
        # Klassisches Würfelproblem-HMM mit fairem & geladenem Würfel
        states = ["F", "L"]
        start_prob = {"F": 0.5, "L": 0.5}
        transition_prob = {
            "F": {"F": 19/20, "L": 1/20},
            "L": {"F": 1/20, "L": 19/20}
        }
        emission_prob = {
            "F": {str(i): 1/6 for i in range(1, 7)},       # fairer Würfel
            "L": {str(i): 0.1 for i in range(1, 6)} | {"6": 0.5}  # geladener Würfel
        }
        return HMM(states, start_prob, transition_prob, emission_prob)

    else:
        # Benutzerdefiniertes HMM erstellen
        num_states = ask_int("Wie viele Zustände hat das HMM?", min_val=1)
        states = [input(f"Name für Zustand {i+1}: ").strip() for i in range(num_states)]

        # Startwahrscheinlichkeiten abfragen
        print("\nStartwahrscheinlichkeiten eingeben (Summe sollte ≈ 1 sein):")
        start_prob = {state: ask_float(f"P(Start = {state})") for state in states}

        # Übergangswahrscheinlichkeiten abfragen
        print("\nÜbergangswahrscheinlichkeiten eingeben:")
        transition_prob = {}
        for from_state in states:
            transition_prob[from_state] = {}
            print(f"Von Zustand '{from_state}':")
            for to_state in states:
                transition_prob[from_state][to_state] = ask_float(f"  P({from_state} → {to_state})")

        # Emissionswahrscheinlichkeiten abfragen
        print("\nEmissionswahrscheinlichkeiten:")
        num_obs = ask_int("Wie viele verschiedene Beobachtungen gibt es?", min_val=1)
        symbols = [input(f"Name für Beobachtung {i+1}: ").strip() for i in range(num_obs)]

        emission_prob = {}
        for state in states:
            emission_prob[state] = {}
            print(f"Für Zustand '{state}':")
            for sym in symbols:
                emission_prob[state][sym] = ask_float(f"  P({state} erzeugt {sym})")

        return HMM(states, start_prob, transition_prob, emission_prob)

def pause(msg="\nDrücke Enter, um fortzufahren...\n"):
    """Kurze Pause, bis der Benutzer Enter drückt."""
    input(msg)

# =============================
# Hauptprogramm
# =============================

def main():
    print("Viterbi-Decoder Tool!")

    # 1. HMM erstellen
    hmm = ask_hmm()

    # 2. Beobachtungssequenz bereitstellen
    mode = ask_choice(
        "Wie möchten Sie die Beobachtungssequenz bereitstellen?", 
        ["Datei einlesen", "Zufällige Sequenz generieren", "Sequenz manuell eingeben"]
    )

    observations = []
    true_states = []

    if mode == "Datei einlesen":
        filepath = input("Pfad zur Datei eingeben (z. B. data/wuerfel2025.txt): ").strip()
        try:
            parser = FileParser()
            observations, true_states = parser.parse_file(filepath)
            print(f"{len(observations)} Beobachtungen geladen: {observations}")
        except Exception as e:
            print(f"Fehler beim Einlesen: {e}")
            return

    elif mode == "Zufällige Sequenz generieren":
        gen_len = ask_int("Länge der Sequenz", min_val=1)
        generator = SequenceGenerator(hmm)
        observations, true_states = generator.generate_sequence(gen_len)
        print(f"Zufällige Sequenz: {observations}")
        print(f"Wahre Zustände:     {true_states}")

    elif mode == "Sequenz manuell eingeben":
        obs_input = input("Gib die Beobachtungssequenz ein (kommagetrennt): ").strip()
        observations = [o.strip() for o in obs_input.split(",") if o.strip()]

    pause()

    # 3. Log-Modus wählen
    use_log = ask_yes_no("Soll mit logarithmischer Wahrscheinlichkeit gerechnet werden?")
    decoder = ViterbiDecoder(hmm, use_log=use_log)

    # 4. Viterbi-Algorithmus ausführen
    print("\nViterbi-Decodierung wird durchgeführt...")
    decoded_states = decoder.decode(observations)

    pause()

    # 5. Ergebnisse ausgeben
    print("\nErgebnis:")
    print("Beobachtungen:", observations)
    print("Vorhergesagt: ", decoded_states)

    if true_states:
        print("\nEchte Zustände:", true_states)

        if decoded_states == true_states:
            print("\nDie vorhergesagten Zustände stimmen EXAKT mit den echten Zuständen überein!")
        else:
            mismatch_count = sum(1 for pred, true in zip(decoded_states, true_states) if pred != true)
            total = len(true_states)
            print("\nDie vorhergesagten Zustände stimmen NICHT mit den echten Zuständen überein.")
            print(f"   → {mismatch_count} von {total} Zuständen sind falsch ({(mismatch_count/total)*100:.2f}%).")

    # 6. Optional: Sequenz umdrehen & erneut dekodieren
    if ask_yes_no("\nMöchten Sie die Sequenz umdrehen und erneut dekodieren?"):
        observations_reversed = list(reversed(observations))

        decoded_states_reversed = decoder.decode(observations_reversed)

        print("\n--- Vergleich Original vs. Umdrehen ---")
        print("Original Vorhersage:   ", decoded_states)
        print("Umdrehte Vorhersage:   ", decoded_states_reversed)

        if (decoded_states_reversed == list(reversed(decoded_states))):
            print("\nDer Viterbi-Pfad der umgedrehten Sequenz ist exakt der umgekehrte Pfad des Originals.")
        else:
            print("\nDer Viterbi-Pfad unterscheidet sich von der einfachen Umkehrung des Originalpfades.")
        print("")

if __name__ == "__main__":
    main()
