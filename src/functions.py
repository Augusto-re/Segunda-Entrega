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


def pasar_a_segundos(duracion):
    partes = duracion.split(":") #Divide en 2 la duracion y lo pone en una lista. Ejemplo: 2:55 lo divide en [2, 5]
    minutos = int(partes[0])
    segundos = int(partes[1])

    return minutos * 60 + segundos

def analizar_canciones(playlist):
    segundos_totales = 0
    max_duracion = playlist[0]
    min_duracion = playlist[0]

    for cancion in playlist:
        segundos = pasar_a_segundos(cancion["duration"])
        segundos_totales += segundos

        if(segundos > pasar_a_segundos(max_duracion["duration"])):
            max_duracion = cancion

        if(segundos < pasar_a_segundos(min_duracion["duration"])):
            min_duracion = cancion
    
    minutos_totales = segundos_totales // 60 #Division entera
    segundos_restantes = segundos_totales % 60 #Lo que resta

    return minutos_totales, segundos_restantes, max_duracion, min_duracion