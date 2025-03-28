import numpy as np

def generar_ciudades(n):
    """Genera n ciudades con coordenadas aleatorias en un espacio 2D (100x100)."""
    return np.random.rand(n, 2) * 100

def guardar_ciudades(ciudades, archivo):
    """Guarda las coordenadas de las ciudades en un archivo de texto."""
    np.savetxt(archivo, ciudades)

def cargar_ciudades(archivo):
    """Carga las coordenadas de las ciudades desde un archivo de texto."""
    return np.loadtxt(archivo)
