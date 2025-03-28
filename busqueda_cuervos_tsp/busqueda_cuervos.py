import os
import numpy as np
import random
import matplotlib.pyplot as plt
from datetime import datetime
from datos_ciudades import generar_ciudades, guardar_ciudades, cargar_ciudades
from evaluacion_rutas import distancia, calcular_distancia_total

def busqueda_cuervos(n_ciudades, root_output_dir, iteraciones=1000):
    """
    Implementa la Búsqueda de Cuervos para resolver el problema del Agente Viajero (TSP).
    """
    output_dir = f"{root_output_dir}/{n_ciudades}_ciudades"
    os.makedirs(output_dir, exist_ok=True)
    
    ciudades = generar_ciudades(n_ciudades)
    guardar_ciudades(ciudades, f"{output_dir}/ciudades_{n_ciudades}.txt")
    
    cuervos = [random.sample(range(n_ciudades), n_ciudades) for _ in range(10)]
    mejores_distancias = []
    
    for _ in range(iteraciones):
        for i in range(len(cuervos)):
            nueva_ruta = cuervos[i][:]
            idx1, idx2 = random.sample(range(n_ciudades), 2)
            nueva_ruta[idx1], nueva_ruta[idx2] = nueva_ruta[idx2], nueva_ruta[idx1]
            
            if calcular_distancia_total(nueva_ruta, ciudades) < calcular_distancia_total(cuervos[i], ciudades):
                cuervos[i] = nueva_ruta
        
        mejores_distancias.append(min(calcular_distancia_total(c, ciudades) for c in cuervos))
    
    grafico_path = f"{output_dir}/grafico_{n_ciudades}.png"
    plt.figure()
    plt.plot(mejores_distancias, label='Distancia mínima')
    plt.xlabel("Iteraciones")
    plt.ylabel("Distancia mínima encontrada")
    plt.title(f"Evolución de la solución TSP con {n_ciudades} ciudades")
    plt.legend()
    plt.grid()
    plt.savefig(grafico_path)
    plt.close()
    
    grafo_path = f"{output_dir}/grafo_{n_ciudades}.png"
    mejor_ruta = min(cuervos, key=lambda c: calcular_distancia_total(c, ciudades))
    graficar_grafo(ciudades, mejor_ruta, grafo_path)
    
    hist_path = f"{output_dir}/histograma_{n_ciudades}.png"
    plt.figure()
    plt.hist([calcular_distancia_total(c, ciudades) for c in cuervos], bins=10, alpha=0.7, color='blue', edgecolor='black')
    plt.xlabel("Distancia total")
    plt.ylabel("Frecuencia")
    plt.title(f"Distribución de distancias - {n_ciudades} ciudades")
    plt.savefig(hist_path)
    plt.close()
    
    generar_reporte_md(n_ciudades, mejores_distancias, mejor_ruta, grafico_path, grafo_path, hist_path, output_dir)
    
    return mejor_ruta, mejores_distancias

def graficar_grafo(ciudades, ruta, filename):
    """Genera un gráfico del mapa de ciudades y su mejor ruta encontrada."""
    plt.figure(figsize=(8, 6))
    for i in range(len(ruta)):
        ciudad_actual = ciudades[ruta[i]]
        ciudad_siguiente = ciudades[ruta[(i + 1) % len(ruta)]]
        plt.plot([ciudad_actual[0], ciudad_siguiente[0]], [ciudad_actual[1], ciudad_siguiente[1]], 'bo-')
    for idx, (x, y) in enumerate(ciudades):
        plt.text(x, y, str(idx), fontsize=12, ha='right', color='red')
    plt.scatter(ciudades[ruta[0]][0], ciudades[ruta[0]][1], color='green', marker='o', s=100, label='Inicio')
    plt.scatter(ciudades[ruta[-1]][0], ciudades[ruta[-1]][1], color='red', marker='o', s=100, label='Fin')
    plt.legend()
    plt.title("Mapa de ciudades y ruta óptima")
    plt.savefig(filename)
    plt.close()

def generar_reporte_md(n_ciudades, mejores_distancias, mejor_ruta, grafico_path, grafo_path, hist_path, output_dir):
    """
    Genera un informe en Markdown con los resultados detallados de la búsqueda.
    """
    md_filename = f"{output_dir}/reporte_{n_ciudades}.md"
    with open(md_filename, "w") as md:
        md.write(f"## Informe de Búsqueda de Cuervos - {n_ciudades} ciudades\n")
        md.write(f"### Mejor ruta encontrada:\n")
        md.write(f"{mejor_ruta}\n\n")
        md.write(f"### Evolución de la distancia mínima por iteraciones:\n")
        md.write(f"![Evolución]({os.path.basename(grafico_path)})\n\n")
        md.write(f"### Mapa de ciudades con la mejor ruta encontrada:\n")
        md.write(f"![Grafo]({os.path.basename(grafo_path)})\n\n")
        md.write(f"### Distribución de distancias obtenidas:\n")
        md.write(f"![Histograma]({os.path.basename(hist_path)})\n\n")
        md.write(f"---\n\n")
    print(f"📄 Informe generado: {md_filename}")

if __name__ == "__main__":
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    root_output_dir = f"resultados/EJECUCION_{timestamp}"
    os.makedirs(root_output_dir, exist_ok=True)
    
    resultados = []
    for n in [20, 50, 100]:
        mejor_ruta, mejores_distancias = busqueda_cuervos(n, root_output_dir)
        resultados.append((n, mejores_distancias))
    
    reporte_general = f"{root_output_dir}/reporte_general.md"
    plt.figure()
    for n, distancias in resultados:
        plt.plot(distancias, label=f"{n} ciudades")
    plt.xlabel("Iteraciones")
    plt.ylabel("Distancia mínima encontrada")
    plt.title("Comparación de evolución de búsqueda para diferentes tamaños de ciudades")
    plt.legend()
    comparacion_path = f"{root_output_dir}/comparacion.png"
    plt.savefig(comparacion_path)
    plt.close()
    
    with open(reporte_general, "w") as md:
        md.write("# Informe General - Comparación entre tamaños de ciudades\n\n")
        md.write(f"![Comparación]({os.path.basename(comparacion_path)})\n\n")
        for n, distancias in resultados:
            md.write(f"## {n} Ciudades\n")
            md.write(f"Mejor distancia encontrada: {min(distancias)}\n\n")
            md.write(f"### Evolución de la distancia mínima:\n")
            md.write(f"![Evolución]({n}_ciudades/grafico_{n}.png)\n\n")
    print(f"📄 Informe comparativo generado: {reporte_general}")
