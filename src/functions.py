def analizar_texto(texto):

    lineas = texto.strip().splitlines()
    total_lineas = len(lineas)

    palabras_por_lineas = [len(linea.split()) for linea in lineas]
    total_palabras = sum(palabras_por_lineas)

    promedio = total_palabras / total_lineas

    lineas_mayores_promedio = []
    for i in range(total_lineas):
        if palabras_por_lineas[i] > promedio:
            lineas_mayores_promedio.append((lineas[i], palabras_por_lineas[i]))

    return total_lineas, total_palabras, promedio, lineas_mayores_promedio


def pasar_a_segundos(duracion):
    partes = duracion.split(
        ":"
    )  # Divide en 2 la duracion y lo pone en una lista. Ejemplo: 2:55 lo divide en [2, 5]
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

        if segundos > pasar_a_segundos(max_duracion["duration"]):
            max_duracion = cancion

        if segundos < pasar_a_segundos(min_duracion["duration"]):
            min_duracion = cancion

    minutos_totales = segundos_totales // 60  # Division entera
    segundos_restantes = segundos_totales % 60  # Lo que resta

    return minutos_totales, segundos_restantes, max_duracion, min_duracion


def dividir_palabras():
    ocultas = input("Ingrese las palabras a ocultar")
    palabras = ocultas.split(",")
    return palabras


def reemplazar_palabra(texto, palabra):
    palabra_minuscula = palabra.strip().lower()
    texto_minuscula = texto.lower()
    resultado = ""
    i = 0

    while i < len(texto):
        fragmento = texto_minuscula[i : i + len(palabra_minuscula)]
        if fragmento == palabra_minuscula:
            resultado += "*" * len(palabra_minuscula)
            i += len(palabra_minuscula)
        else:
            resultado += texto[i]
            i += 1
    return resultado


def tapar_spoileres(texto, palabras):
    for palabra in palabras:
        texto = reemplazar_palabra(texto, palabra)
    return texto


# Aca empieza lo del punto 10


def calcular_puntaje_ronda(jueces):
    return sum(jueces.values())


def obtener_ganador_ronda(puntajes_ronda):
    return max(puntajes_ronda, key=puntajes_ronda.get)


def actualizar_estadisticas(estadisticas, nombre, puntaje):
    estadisticas[nombre]["total"] += puntaje
    estadisticas[nombre]["puntajes_por_ronda"].append(puntaje)
    if puntaje > estadisticas[nombre]["mejor_ronda"]:
        estadisticas[nombre]["mejor_ronda"] = puntaje


def ordenar_por_total(participantes, estadisticas):
    pares = []
    for nombre in participantes:
        pares.append((estadisticas[nombre]["total"], nombre))

    pares.sort(reverse=True)

    ranking = []
    for puntaje, nombre in pares:
        ranking.append(nombre)

    return ranking


def imprimir_tabla_progreso(
    numero, tema, ganador, puntaje_ganador, participantes, estadisticas, puntajes_ronda
):
    print(f"\nRonda {numero} - {tema}:")
    print(f"  Ganador: {ganador} ({puntaje_ganador} pts)")
    ranking = ordenar_por_total(participantes, estadisticas)
    print(f"  {'Pos':<5} {'Cocinero':<12} {'Esta ronda':<12} {'Total acumulado'}")
    print(f"  {'-'*45}")
    for pos, nombre in enumerate(ranking, start=1):
        print(
            f"  {pos:<5} {nombre:<12} {puntajes_ronda[nombre]:<12} {estadisticas[nombre]['total']}"
        )


def imprimir_tabla_final(participantes, estadisticas, total_rondas):
    print("\n" + "=" * 62)
    print("Tabla de posiciones final:")
    print(
        f"{'Cocinero':<12} {'Puntaje':>8} {'Rondas ganadas':>15} {'Mejor ronda':>12} {'Promedio':>10}"
    )
    print("-" * 62)
    ranking = ordenar_por_total(participantes, estadisticas)
    for nombre in ranking:
        s = estadisticas[nombre]
        promedio = s["total"] / total_rondas
        print(
            f"{nombre:<12} {s['total']:>8} {s['rondas_ganadas']:>15} {s['mejor_ronda']:>12} {promedio:>10.1f}"
        )
    print("-" * 62)


def simular_competencia(rounds):
    participantes = list(
        rounds[0]["scores"].keys()
    )  # Creo un diccionario con los participantes para guardar despues sus estadisticas

    estadisticas = {
        nombre: {
            "total": 0,
            "rondas_ganadas": 0,
            "mejor_ronda": 0,
            "puntajes_por_ronda": [],
        }
        for nombre in participantes
    }

    for i, ronda in enumerate(rounds, start=1):
        puntaje_ronda = {}
        for nombre, jueces in ronda["scores"].items():
            puntaje = calcular_puntaje_ronda(jueces)
            puntaje_ronda[nombre] = puntaje
            actualizar_estadisticas(estadisticas, nombre, puntaje)
        ganador = obtener_ganador_ronda(puntaje_ronda)
        estadisticas[ganador]["rondas_ganadas"] += 1
        imprimir_tabla_progreso(
            i,
            ronda["theme"],
            ganador,
            puntaje_ronda[ganador],
            participantes,
            estadisticas,
            puntaje_ronda,
        )
    imprimir_tabla_final(participantes, estadisticas, len(rounds))
