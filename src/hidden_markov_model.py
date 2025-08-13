import math
from typing import List, Dict, Mapping

class HMM:
    def __init__(
        self,
        states: List[str],
        start_probabilities: Dict[str, float],
        transition_probabilities: Dict[str, Dict[str, float]],
        emission_probabilities: Dict[str, Dict[str, float]]
    ):
        # Zustände des HMM (z. B. "F" für fairer Würfel, "L" für gezinkter Würfel)
        self.states = states

        # Startwahrscheinlichkeiten für jeden Zustand
        self._start = start_probabilities

        # Übergangswahrscheinlichkeiten zwischen den Zuständen
        self._transitions = transition_probabilities

        # Emissionswahrscheinlichkeiten: Wahrscheinlichkeit, ein Symbol in einem Zustand zu beobachten
        self._emissions = emission_probabilities

        # Prüfen, ob das HMM korrekt definiert ist
        self._validate_model()

    def _validate_model(self):
        """
        Prüft, ob für alle definierten Zustände
        Start-, Übergangs- und Emissionswahrscheinlichkeiten vorhanden sind.
        """
        for state in self.states:
            if state not in self._start:
                raise ValueError(f"Startwahrscheinlichkeit fehlt für Zustand: {state}")
            if state not in self._transitions:
                raise ValueError(f"Übergangswahrscheinlichkeiten fehlen für Zustand: {state}")
            if state not in self._emissions:
                raise ValueError(f"Emissionswahrscheinlichkeiten fehlen für Zustand: {state}")    
        
    # ---------- Getter ----------
    def get_emission_row(self, state: str) -> dict:
        """
        Gibt die Emissionswahrscheinlichkeiten für einen Zustand zurück.
        """
        return dict(self._emissions[state])

    def get_transition_row(self, state: str) -> dict:
        """
        Gibt die Übergangswahrscheinlichkeiten vom angegebenen Zustand zu allen anderen Zuständen zurück.
        """
        return dict(self._transitions[state])

    # ---------- Zugriff auf normale Wahrscheinlichkeiten ----------
    def get_start_prob_normal(self, state: str) -> float:
        """Gibt die Startwahrscheinlichkeit für einen Zustand zurück (normaler Wert, nicht im Log)."""
        return self._start[state]

    def get_transition_prob_normal(self, from_state: str, to_state: str) -> float:
        """Gibt die Übergangswahrscheinlichkeit von einem Zustand zu einem anderen zurück (normaler Wert)."""
        return self._transitions[from_state][to_state]
    
    def get_emission_prob_normal(self, state: str, symbol: str) -> float:
        """
        Gibt die Emissionswahrscheinlichkeit zurück, ein Symbol in einem Zustand zu beobachten.
        Falls das Symbol im Zustand nicht vorkommt, wird ein Fehler geworfen.
        """
        try:
            return self._emissions[state][symbol]
        except KeyError:
            raise ValueError(f"Symbol '{symbol}' nicht im Emissionsmodell für Zustand '{state}' enthalten.")
        
    # ---------- Zugriff auf Log-Wahrscheinlichkeiten ----------
    def get_start_prob_log(self, state: str) -> float:
        """Gibt die Startwahrscheinlichkeit im Logarithmus zurück."""
        return self._to_log(self._start[state])

    def get_transition_prob_log(self, from_state: str, to_state: str) -> float:
        """Gibt die Übergangswahrscheinlichkeit im Logarithmus zurück."""
        return self._to_log(self._transitions[from_state][to_state])
    
    def get_emission_prob_log(self, state: str, symbol: str) -> float:
        """Gibt die Emissionswahrscheinlichkeit im Logarithmus zurück."""
        try:
            return self._to_log(self._emissions[state][symbol])
        except KeyError:
            raise ValueError(f"Symbol '{symbol}' nicht im Emissionsmodell für Zustand '{state}' enthalten.")
        
    def _to_log(self, value: float) -> float:
        """
        Hilfsmethode zum Umrechnen einer Wahrscheinlichkeit in den Logarithmus.
        Falls die Wahrscheinlichkeit 0 oder kleiner ist, wird -∞ zurückgegeben.
        """
        if value <= 0.0:
            return float("-inf")
        return math.log(value)

