def convertir_a_minutos_y_segundos(numero):
    minutos = int(numero // 60)
    segundos = int(numero % 60)
    centesimas = int((numero % 1) * 100)
    milesimas = int((numero % 0.01) * 1000)
    return minutos,"minutes",segundos,"seconds",centesimas,"centesimas",milesimas,"milesimas"