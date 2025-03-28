from busqueda_cuervos import busqueda_cuervos

if __name__ == "__main__":
    # Ejecutar el algoritmo para 20, 50 y 100 ciudades
    for n in [20, 50, 100]:
        mejor_ruta, ciudades = busqueda_cuervos(n)
        print(f"Mejor ruta encontrada para {n} ciudades: {mejor_ruta}")
