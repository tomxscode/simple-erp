def validar_rut(rut):
    rut = rut.replace(".", "").replace("-", "").upper()
    
    if not rut[:-1].isdigit():
        return False
    
    rut_numeros = list(map(int, rut[:-1]))
    factor = 2
    suma = sum([num * factor for num in reversed(rut_numeros)])
    verificador_calculado = 11 - (suma % 11)
    
    if verificador_calculado == 11:
        verificador_calculado = 0
    elif verificador_calculado == 10:
        verificador_calculado = 'K'
    
    return str(verificador_calculado) == rut[-1]
