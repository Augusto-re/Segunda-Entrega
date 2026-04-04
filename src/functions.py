def analizar_texto(texto):

    
    lineas = texto.strip().splitlines()
    total_lineas = len(lineas)

    palabras_por_lineas = [len(linea.split()) for linea in lineas]
    total_palabras = sum(palabras_por_lineas)

    promedio = total_palabras / total_lineas

    lineas_mayores_promedio = []
    for i in range(total_lineas):
        if(palabras_por_lineas[i] > promedio):
            lineas_mayores_promedio.append((lineas[i], palabras_por_lineas[i]))


    return total_lineas, total_palabras, promedio, lineas_mayores_promedio