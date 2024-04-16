def convertir_a_min_seg_centesimas_milesimas(numero):
    minutos = numero // 60
    segundos = numero % 60
    centesimas = int((numero % 1) * 100)
    milesimas = int((numero % 0.01) * 1000)
    return minutos,"minutes",segundos,"seconds",centesimas,"centesimas",milesimas,"milesimas"

numero_total = 1250  # Ejemplo de un número total de segundos
convertir_a_min_seg_centesimas_milesimas(120)