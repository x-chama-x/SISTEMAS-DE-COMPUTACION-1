# programa que convierte una cadena de bits a su representación en punto flotante dependiendo de la mantisa


def calcular_bits_exponente(cadena_bits, cant_bits_mantisa):
    return len(cadena_bits) - cant_bits_mantisa

def obtener_signo_mantisa():
    tipo_signo = input("¿La mantisa es con signo (BCS) o sin signo (BSS)? ")
    if tipo_signo == "BCS":
        return 1
    elif tipo_signo == "BSS":
        return 0
    else:
        print("Tipo de signo inválido. Por favor, ingrese 'BCS' o 'BSS'.")
        return obtener_signo_mantisa()

def obtener_signo_exponente():
    tipo_signo = input("¿El exponente es con signo (BCS) o sin signo (BSS)? ")
    if tipo_signo == "BCS":
        return 1
    elif tipo_signo == "BSS":
        return 0
    else:
        print("Tipo de signo inválido. Por favor, ingrese 'BCS' o 'BSS'.")
        return obtener_signo_exponente()

def obtener_tipo_mantisa():
    tipo = input("¿La mantisa es a complemento 1 (C1), complemento a 2 (C2) o ninguno (N)? Ingrese 'C1', 'C2' o 'N': ")
    if tipo == 'C1':
        return 1
    elif tipo == 'C2':
        return 0
    elif tipo == 'N':
        return 3
    else:
        print("Entrada no válida. Por favor, ingrese 'C1', 'C2' o 'N'.")
        return obtener_tipo_mantisa()

def obtener_tipo_exponente():
    tipo = input("¿El exponente es a complemento 1 (C1), complemento a 2 (C2) o ninguno (N)? Ingrese 'C1', 'C2' o 'N': ")
    if tipo == 'C1':
        return 1
    elif tipo == 'C2':
        return 0
    elif tipo == 'N':
        return 3
    else:
        print("Entrada no válida. Por favor, ingrese 'C1', 'C2' o 'N'.")
        return obtener_tipo_exponente()

def convertir_mantisa_decimal(cadena_bits, con_signo, tipo_mantisa):
    if tipo_mantisa == 1:  # Complemento a 1
        # Invertir los bits
        bits_invertidos = ''.join('1' if bit == '0' else '0' for bit in cadena_bits)
        valor_decimal = int(bits_invertidos, 2)
        return -valor_decimal if cadena_bits[0] == '1' else valor_decimal
    elif tipo_mantisa == 0:  # Complemento a 2
        # Invertir los bits y sumar 1
        bits_invertidos = ''.join('1' if bit == '0' else '0' for bit in cadena_bits)
        valor_decimal = int(bits_invertidos, 2) + 1
        return -valor_decimal if cadena_bits[0] == '1' else valor_decimal
    elif tipo_mantisa == 3:  # Ninguno
        if con_signo:
            signo = -1 if cadena_bits[0] == '1' else 1
            valor_decimal = int(cadena_bits[1:], 2)
            return signo * valor_decimal
        else:
            return int(cadena_bits, 2)

def convertir_exponente_decimal(cadena_bits, con_signo, tipo_exponente):
    if con_signo:
        signo = -1 if cadena_bits[0] == '1' else 1
        cadena_bits = cadena_bits[1:]  # Removemos el bit de signo
    else:
        signo = 1

    if tipo_exponente == 1:  # Complemento a 1
        if con_signo:
            valor_decimal = int(cadena_bits, 2)
            if signo == -1:
                valor_decimal = ~valor_decimal & ((1 << len(cadena_bits)) - 1)  # Invertir bits
        else:
            bits_invertidos = ''.join('1' if bit == '0' else '0' for bit in cadena_bits)
            valor_decimal = int(bits_invertidos, 2)
    elif tipo_exponente == 0:  # Complemento a 2
        if con_signo:
            valor_decimal = int(cadena_bits, 2)
            if signo == -1:
                valor_decimal = (~valor_decimal + 1) & ((1 << len(cadena_bits)) - 1)  # Invertir bits y sumar 1
        else:
            bits_invertidos = ''.join('1' if bit == '0' else '0' for bit in cadena_bits)
            valor_decimal = int(bits_invertidos, 2) + 1
    elif tipo_exponente == 3:  # Ninguno
        valor_decimal = int(cadena_bits, 2)
    
    return signo * valor_decimal
        
def calcular_mantisa_fraccionaria(cadena_bits, cant_bits_mantisa, signo_mantisa):
    if signo_mantisa:
        # Extraer el bit de signo
        bit_signo = cadena_bits[0]
        
        # Extraer la mantisa sin el bit de signo
        mantisa = cadena_bits[1:cant_bits_mantisa]
    else:
        # No considerar el bit de signo
        bit_signo = '0'
        mantisa = cadena_bits[:cant_bits_mantisa]
    
    # Agregar '0.' delante de la mantisa
    mantisa_fraccionaria = '0.' + mantisa
    
    # Convertir la mantisa fraccionaria a decimal
    valor_fraccionario = 0
    for i, bit in enumerate(mantisa):
        if bit == '1':
            valor_fraccionario += 2 ** -(i + 1)
    
    # Aplicar el signo si es necesario
    if bit_signo == '1':
        valor_fraccionario = -valor_fraccionario
    
    return valor_fraccionario


def calcular_representacion_de_pto_flotante_con_mantisa_fraccionaria_con_bit_implicito(mantisa, cadena_bits, cant_bits_mantisa, signo_mantisa, signo_exponente, tipo_exponente):
    # Convertir la mantisa a un valor decimal
    valor_mantisa = 0  # El bit implícito
    for i, bit in enumerate(mantisa[2:], 1):  # Ignoramos '0.' al principio
        if bit == '1':
            valor_mantisa += 2 ** -i

    # Convertir el exponente a decimal
    valor_exponente = convertir_exponente_decimal(cadena_bits[cant_bits_mantisa:], signo_exponente, tipo_exponente)
    
    # Calcular la representación en punto flotante
    base = 2
    resultado = valor_mantisa * (base ** valor_exponente)

    return resultado


def calcular_representacion_de_pto_flotante_con_mantisa_fraccionaria(cadena_bits, cant_bits_mantisa, signo_mantisa, signo_exponente, tipo_exponente):
    # Calcular la mantisa fraccionaria
    mantisa_fraccionaria = calcular_mantisa_fraccionaria(cadena_bits, cant_bits_mantisa, signo_mantisa)
    
    # Convertir el exponente a decimal
    valor_exponente = convertir_exponente_decimal(cadena_bits[cant_bits_mantisa:], signo_exponente, tipo_exponente)
    
    # Calcular la representación en punto flotante
    base = 2
    resultado = mantisa_fraccionaria * (base ** valor_exponente)
    return resultado


def calcular_representacion_de_pto_flotante(mantisa, exponente, signo_mantisa, signo_exponente, tipo_mantisa, tipo_exponente):
    # Convertir la mantisa y el exponente a valores decimales teniendo en cuenta el tipo de complemento
    valor_mantisa = convertir_mantisa_decimal(mantisa, signo_mantisa, tipo_mantisa)
    valor_exponente = convertir_exponente_decimal(exponente, signo_exponente, tipo_exponente)
    
    # Calcular la representación en punto flotante
    base = 2
    resultado = valor_mantisa * (base ** valor_exponente)

    # imprimir datos de depuración
    print("Mantisa:", valor_mantisa)
    print("Exponente:", valor_exponente)
    
    return resultado

def mantisa_esta_normalizada(mantisa, es_bcs):
    if es_bcs:
        # Evaluar el segundo bit más significativo
        if mantisa[1] == '0':
            return 0
        else:
            return 1
    else:
        # Evaluar el primer bit más significativo
        if mantisa[0] == '0':
            return 0
        else:
            return 1

def agregar_bit_implicito(mantisa):
    return '0.1' + mantisa


def imprimir_si_mantisa_fraccionaria_normalizada(mantisa, es_bcs):
    if mantisa_esta_normalizada(mantisa, es_bcs):
        print("La mantisa fraccionaria está normalizada, se puede representar en punto flotante con mantisa fraccionaria normalizada.")
        print("la representación es igual La representación en punto flotante con mantisa fraccionaria.")
    else:
        print("No se puede representar en punto flotante con mantisa fraccionaria normalizada, ya que la Mantisa no está normalizada!")

def obtener_cadena_bits_valida():
    def validar_cadena_bits(cadena):
        if len(cadena) > 50:
            return False
        for char in cadena:
            if char not in ('0', '1'):
                return False
        return True

    cadena_bits = input("Ingrese la cadena de bits: ")
    while not validar_cadena_bits(cadena_bits):
        print("Cadena inválida. Asegúrese de que la cadena no tenga más de 50 bits y solo contenga '0' y '1'.")
        cadena_bits = input("Ingrese la cadena de bits: ")
    return cadena_bits

def obtener_cant_bits_mantisa_valida(cadena_bits):
    def validar_cant_bits_mantisa(cant_bits_mantisa, longitud_cadena):
        return 0 < cant_bits_mantisa < longitud_cadena

    cant_bits_mantisa = int(input("Ingrese la cantidad de bits de la mantisa: "))
    while not validar_cant_bits_mantisa(cant_bits_mantisa, len(cadena_bits)):
        print(f"Cantidad inválida. Asegúrese de que la cantidad de bits de la mantisa sea mayor a 0 y menor a {len(cadena_bits)}.")
        cant_bits_mantisa = int(input("Ingrese la cantidad de bits de la mantisa: "))
    return cant_bits_mantisa

# programa principal
cadena_bits = obtener_cadena_bits_valida()
cant_bits_mantisa = obtener_cant_bits_mantisa_valida(cadena_bits)
cant_bits_exponente = calcular_bits_exponente(cadena_bits, cant_bits_mantisa)
signo_mantisa = obtener_signo_mantisa()
signo_exponente = obtener_signo_exponente()
tipo_mantisa = obtener_tipo_mantisa()
tipo_exponente = obtener_tipo_exponente()
rep_punto_flotante = calcular_representacion_de_pto_flotante(cadena_bits[:cant_bits_mantisa], cadena_bits[cant_bits_mantisa:], signo_mantisa, signo_exponente, tipo_mantisa, tipo_exponente)
print("La representación en punto flotante es:", rep_punto_flotante)
rep_punto_flotante_fraccionaria = calcular_representacion_de_pto_flotante_con_mantisa_fraccionaria(cadena_bits, cant_bits_mantisa, signo_mantisa, signo_exponente, tipo_exponente)
print("La representación en punto flotante con mantisa fraccionaria es:", rep_punto_flotante_fraccionaria)
imprimir_si_mantisa_fraccionaria_normalizada(cadena_bits[:cant_bits_mantisa], signo_mantisa)
mantisa_con_bit_implicito = agregar_bit_implicito(cadena_bits[:cant_bits_mantisa])
rep_punto_flotante_con_bit_implicito = calcular_representacion_de_pto_flotante_con_mantisa_fraccionaria_con_bit_implicito(mantisa_con_bit_implicito, cadena_bits, cant_bits_mantisa, signo_mantisa, signo_exponente, tipo_exponente)
print("La representación en punto flotante con mantisa con bit implícito es:", rep_punto_flotante_con_bit_implicito)

