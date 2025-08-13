from typing import List, Dict
import sys
import os

from src.hidden_markov_model import HMM

class ViterbiDecoder:
    def __init__(self, hmm: HMM, use_log: bool = False):
        # HMM-Objekt speichern und einstellen, ob Log-Wahrscheinlichkeiten genutzt werden sollen
        self.hmm = hmm
        self.use_log = use_log

    def decode(self, observations: List[str]) -> List[str]:
        """
        Führt den Viterbi-Algorithmus aus, um die wahrscheinlichste
        Zustandsfolge für eine gegebene Beobachtungssequenz zu finden.
        """
        if not observations:
            return []
        
        V = [{}]  # Matrix für Wahrscheinlichkeiten (pro Zustand, pro Zeit)
        path: Dict[str, List[str]] = {}  # Speichert den bisher besten Pfad für jeden Zustand

        # --- 1. Initialisierung (t = 0) ---
        for state in self.hmm.states:
            if self.use_log:
                # Startwahrscheinlichkeit + Emissionswahrscheinlichkeit (Log-Form)
                start_p = self.hmm.get_start_prob_log(state)
                emit_p = self.hmm.get_emission_prob_log(state, observations[0])
                V[0][state] = start_p + emit_p
                print(f"V[{state}] = log({start_p:.4f}) + log({emit_p:.4f}) = {V[0][state]:.4f}")
            else:
                # Startwahrscheinlichkeit × Emissionswahrscheinlichkeit (Normalform)
                start_p = self.hmm.get_start_prob_normal(state)
                emit_p = self.hmm.get_emission_prob_normal(state, observations[0])
                V[0][state] = start_p * emit_p
                print(f"V[{state}] = {start_p:.4f} * {emit_p:.4f} = {V[0][state]:.6f}")

            # Anfangspfad für diesen Zustand
            path[state] = [state]

        # --- 2. Rekursion (t > 0) ---
        for t in range(1, len(observations)):
            V.append({})
            new_path: Dict[str, List[str]] = {}

            # Für jeden möglichen aktuellen Zustand den besten vorherigen Zustand finden
            for curr_state in self.hmm.states:
                max_prob, best_prev = self._get_best_previous_state(
                    V, t, curr_state, observations[t]
                )
                V[t][curr_state] = max_prob
                new_path[curr_state] = path[best_prev] + [curr_state]

            # Pfade für die nächste Iteration aktualisieren
            path = new_path  

        # --- 3. Termination: besten Endzustand wählen ---
        last_probs = V[-1]
        final_state = max(last_probs, key=last_probs.get)
        return path[final_state]
    
    def _get_best_previous_state(self, V: List[Dict[str, float]], t: int, curr_state: str, observation: str):
        """
        Hilfsmethode: Ermittelt für einen aktuellen Zustand den vorherigen Zustand,
        der zur höchsten Wahrscheinlichkeit führt.
        """
        best_prob = float("-inf") if self.use_log else 0.0
        best_prev_state = None

        print(f"\n[t={t}] Zielzustand: {curr_state} | Beobachtung: {observation}")

        for prev_state in self.hmm.states:
            prev_v = V[t - 1][prev_state]

            if self.use_log:
                # Log-Variante: Wahrscheinlichkeiten addieren
                trans_prob = self.hmm.get_transition_prob_log(prev_state, curr_state)
                emit_prob = self.hmm.get_emission_prob_log(curr_state, observation)
                prob = prev_v + trans_prob + emit_prob
                print(f"  {prev_state} → {curr_state}: {prev_v:.4f} + {trans_prob:.4f} + {emit_prob:.4f} = {prob:.4f}")
            else:
                # Normalform: Wahrscheinlichkeiten multiplizieren
                trans_prob = self.hmm.get_transition_prob_normal(prev_state, curr_state)
                emit_prob = self.hmm.get_emission_prob_normal(curr_state, observation)
                prob = prev_v * trans_prob * emit_prob
                print(f"  {prev_state} → {curr_state}: {prev_v:.6f} * {trans_prob:.4f} * {emit_prob:.4f} = {prob:.6f}")

            # Prüfen, ob dies der bisher beste vorherige Zustand ist
            if prob > best_prob:
                best_prob = prob
                best_prev_state = prev_state

        if best_prev_state is None:
            raise ValueError("Kein gültiger Pfad gefunden.")
        
        print(f"  ➤ Bester vorheriger Zustand: {best_prev_state} mit Wahrscheinlichkeit {best_prob:.6f}")
        return best_prob, best_prev_state
