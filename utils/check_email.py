import re

def validar_email(email):
    # Expresión regular para validar un correo electrónico
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    # Comprobar si el correo electrónico coincide con el patrón
    if re.match(patron, email):
        return True
    else:
        return False