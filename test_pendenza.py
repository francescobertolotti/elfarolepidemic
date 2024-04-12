import numpy as np

# Array di valori costanti
y = np.array([100, 100, 100])

# Creazione di un array x con gli stessi valori di y (può essere qualsiasi cosa in questo caso)
x = np.arange(len(y))

# Adattamento di una retta (polinomio di primo grado)
coefficients = np.polyfit(x, y, 1)

# La pendenza della retta è il primo coefficiente
pendenza = coefficients[0]
print("La pendenza della retta è:", pendenza)


def find_possible_actions(states_dict, target_states):
    possible_actions = []
    for action, state in states_dict.items():
        if state[0] == target_states[0] and state[2] == target_states[1]:
            possible_actions.append(action)
    return possible_actions

# Dizionario di azioni con relativi stati
actions_dict = {0: (1, 0, 1), 1: (1, 1, 0), 2: (0, 1, 1)}

# Stati da cercare
target_states = (1, 1)  # Stato_1 e stato_3 attivi

# Trova le azioni possibili per gli stati target
possible_actions = find_possible_actions(actions_dict, target_states)

print("Azioni possibili:", possible_actions)
