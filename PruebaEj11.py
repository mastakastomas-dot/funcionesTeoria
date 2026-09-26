from Funciones import *


alfabeto = ['a', 'b', 'c']
probabilidades = [1/4, 1/4, 1/2]

alfa_2, probs_2 = extension(alfabeto, probabilidades, 2)
alfa_3, probs_3 = extension(alfabeto, probabilidades, 3)

entriopia_2 = entriopia(probs_2)
entriopia_3 = entriopia(probs_3)

print(alfa_2)
print("Entriopia: ", entriopia_2)
print(alfa_3)
print("Entriopia: ", entriopia_3)
print("Entriopia original: ", entriopia(probabilidades))



