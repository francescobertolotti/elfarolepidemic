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