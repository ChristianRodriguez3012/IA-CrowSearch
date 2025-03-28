import numpy as np

def distancia(ciudad1, ciudad2):
    """Calcula la distancia euclidiana entre dos ciudades."""
    return np.linalg.norm(ciudad1 - ciudad2)

def calcular_distancia_total(ruta, ciudades):
    """Calcula la distancia total de una ruta en el problema del agente viajero."""
    distancia_total = sum(distancia(ciudades[ruta[i]], ciudades[ruta[i+1]]) for i in range(len(ruta) - 1))
    distancia_total += distancia(ciudades[ruta[-1]], ciudades[ruta[0]])  # Regreso a la ciudad inicial
    return distancia_total
