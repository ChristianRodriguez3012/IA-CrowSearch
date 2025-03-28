import os
import numpy as np
import random
import matplotlib.pyplot as plt
from datetime import datetime
from datos_ciudades import generar_ciudades, guardar_ciudades, cargar_ciudades
from evaluacion_rutas import distancia, calcular_distancia_total
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def busqueda_cuervos(n_ciudades, iteraciones=1000, memoria_max=10, coef_aprendizaje=0.1):
    """
    Implementa la Búsqueda de Cuervos para resolver el problema del Agente Viajero (TSP).
    """

    # Crear carpeta de resultados con timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_dir = f"resultados/{n_ciudades}_ciudades-{timestamp}"
    os.makedirs(output_dir, exist_ok=True)
    
    # Generamos un conjunto de ciudades aleatorias y lo guardamos en un archivo
    ciudades = generar_ciudades(n_ciudades)
    guardar_ciudades(ciudades, f"{output_dir}/ciudades_{n_ciudades}.txt")
    
    # Inicializamos la población de cuervos con rutas aleatorias
    cuervos = [random.sample(range(n_ciudades), n_ciudades) for _ in range(10)]
    memoria = cuervos.copy()  # Cada cuervo recuerda su mejor solución
    mejores_distancias = []  # Lista para almacenar la mejor distancia en cada iteración
    
    # Iniciamos el proceso iterativo de búsqueda
    for _ in range(iteraciones):
        for i in range(len(cuervos)):
            referencia = random.choice(memoria)  # Escogemos una ruta de referencia en la memoria
            nueva_ruta = cuervos[i][:]  # Creamos una copia de la ruta actual
            
            # Intercambiamos dos ciudades de la ruta para generar una nueva solución
            idx1, idx2 = random.sample(range(n_ciudades), 2)
            nueva_ruta[idx1], nueva_ruta[idx2] = nueva_ruta[idx2], nueva_ruta[idx1]
            
            # Si la nueva ruta es mejor, actualizamos el cuervo y su memoria
            if calcular_distancia_total(nueva_ruta, ciudades) < calcular_distancia_total(cuervos[i], ciudades):
                cuervos[i] = nueva_ruta
                memoria[i] = nueva_ruta
        
        # Guardamos la mejor distancia encontrada en esta iteración
        mejores_distancias.append(min(calcular_distancia_total(c, ciudades) for c in cuervos))
    
    # Seleccionamos la mejor ruta después de todas las iteraciones
    mejor_ruta = min(cuervos, key=lambda c: calcular_distancia_total(c, ciudades))

    # Guardamos la gráfica de evolución de la búsqueda
    grafico_path = f"{output_dir}/grafico_{n_ciudades}.png"
    plt.plot(mejores_distancias)
    plt.xlabel("Iteraciones")
    plt.ylabel("Distancia mínima encontrada")
    plt.title(f"Evolución de la solución TSP con {n_ciudades} ciudades")
    plt.savefig(grafico_path)  
    plt.close()
    
    # Graficar el mapa de ciudades con la mejor ruta
    grafo_path = f"{output_dir}/grafo_{n_ciudades}.png"
    graficar_grafo(ciudades, mejor_ruta, grafo_path)

    # Generamos el reporte
    generar_reporte(n_ciudades, mejores_distancias, mejor_ruta, grafico_path, grafo_path, output_dir)

    return mejor_ruta, ciudades

def graficar_grafo(ciudades, ruta, filename):
    """Genera un gráfico del mapa de ciudades y su mejor ruta encontrada."""
    plt.figure(figsize=(8, 6))
    for i in range(len(ruta)):
        ciudad_actual = ciudades[ruta[i]]
        ciudad_siguiente = ciudades[ruta[(i + 1) % len(ruta)]]
        plt.plot([ciudad_actual[0], ciudad_siguiente[0]], [ciudad_actual[1], ciudad_siguiente[1]], 'bo-')
    for idx, (x, y) in enumerate(ciudades):
        plt.text(x, y, str(idx), fontsize=12, ha='right')
    plt.title("Mapa de ciudades y ruta óptima")
    plt.savefig(filename)
    plt.close()

def generar_reporte(n_ciudades, mejores_distancias, mejor_ruta, grafico_path, grafo_path, output_dir):
    """
    Genera un informe en PDF con los resultados de la búsqueda.
    """
    pdf_filename = f"{output_dir}/reporte_{n_ciudades}.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, 750, f"Informe de Búsqueda de Cuervos - {n_ciudades} ciudades")
    c.setFont("Helvetica", 12)
    c.drawString(100, 720, "Mejor ruta encontrada:")
    
    # Formateo de la ruta con saltos de línea
    ruta_texto = " → ".join(map(str, mejor_ruta))
    lines = [ruta_texto[i:i+80] for i in range(0, len(ruta_texto), 80)]  
    y_pos = 700
    for line in lines:
        c.drawString(100, y_pos, line)
        y_pos -= 20
    
    # Incluir imágenes del gráfico de evolución y el grafo de ciudades
    c.drawImage(grafico_path, 100, y_pos - 200, width=400, height=200)
    c.drawImage(grafo_path, 100, y_pos - 450, width=400, height=200)
    
    c.save()
    print(f"📄 Reporte generado: {pdf_filename}")

if __name__ == "__main__":
    for n in [20, 50, 100]:
        mejor_ruta, ciudades = busqueda_cuervos(n)
        print(f"Mejor ruta encontrada para {n} ciudades: {mejor_ruta}")
