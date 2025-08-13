import random
from typing import List, Tuple
import sys
import os

from src.hidden_markov_model import HMM

class SequenceGenerator:
    def __init__(self, hmm: HMM):
        # Das HMM-Objekt, mit dem die Sequenzen generiert werden
        self.hmm = hmm

    def generate_sequence(self, length: int) -> Tuple[List[str], List[str]]:
        """
        Generiert eine Zufallssequenz basierend auf dem HMM.
        Gibt zwei Listen zurück:
        - observations: erzeugte Beobachtungssymbole
        - states: die tatsächlichen Zustände, die für die Beobachtungen verantwortlich waren
        """
        states = []
        observations = []

        # Startzustand wählen basierend auf den Startwahrscheinlichkeiten des HMM
        start_state = self._weighted_choice({
            state: self.hmm.get_start_prob_normal(state)
            for state in self.hmm.states
        })
        states.append(start_state)

        # Erste Emission aus dem Startzustand generieren
        first_obs = self._weighted_choice(self.hmm.get_emission_row(start_state))
        observations.append(first_obs)

        # Wiederholt: neuen Zustand und zugehörige Emission erzeugen
        current_state = start_state
        for _ in range(1, length):
            # Übergang zum nächsten Zustand (gewichtete Zufallsauswahl)
            current_state = self._weighted_choice(self.hmm.get_transition_row(current_state))
            states.append(current_state)

            # Neue Beobachtung aus dem aktuellen Zustand erzeugen
            obs = self._weighted_choice(self.hmm.get_emission_row(current_state))
            observations.append(obs)

        return observations, states

    def _weighted_choice(self, distribution: dict) -> str:
        """
        Wählt zufällig ein Element aus einer Wahrscheinlichkeitsverteilung (dictionary).
        - distribution: {Element: Wahrscheinlichkeit}
        """
        elements = list(distribution.keys())    # Mögliche Optionen
        weights = list(distribution.values())   # Zugehörige Wahrscheinlichkeiten
        return random.choices(elements, weights=weights, k=1)[0]


