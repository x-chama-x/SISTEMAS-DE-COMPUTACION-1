import sys
import os

# Función para limpiar la pantalla
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# FUNCIONES DUPLICADAS DE CONVERSION DE DECIMAL A BINARIO

def decimal_to_binary(decimal, bits):
    binary = format(abs(decimal), f'b')
    if decimal < 0:
        binary = binary.zfill(bits)
    return binary

def decimal_to_binario(decimal, bits):
    # Convertir el número decimal a binario y eliminar el prefijo '0b'
    binario = bin(decimal)[2:]
    # Rellenar con ceros a la izquierda para asegurar la cantidad de bits
    binario = binario.zfill(bits)
    return binario


def decimal_fraccionario_a_binario_fraccionario(num):
    if num == 0:
        return "0.0"
    
    signo = '-' if num < 0 else ''
    num = abs(num)
    entero, decimal = str(num).split('.')
    entero = int(entero)
    decimal = float("0." + decimal)
    
    binario_entero = bin(entero)[2:]
    
    binario_decimal = ""
    precision = 23
    while decimal > 0 and len(binario_decimal) < precision:
        decimal *= 2
        if decimal >= 1:
            binario_decimal += "1"
            decimal -= 1
        else:
            binario_decimal += "0"
    
    return f"{signo}{binario_entero}.{binario_decimal}"


# FUNCIONES DE CONVERSION PUNTO FLOTANTE

def calcular_bits_exponente(cadena_bits, cant_bits_mantisa):
    return len(cadena_bits) - cant_bits_mantisa

def complemento_a_1(cadena_bits):
    # Invertir cada bit de la cadena
    complemento1 = ''.join('1' if bit == '0' else '0' for bit in cadena_bits)
    return complemento1

def complemento_a_2(cadena_bits):
    # Obtener el complemento a 1
    complemento1 = complemento_a_1(cadena_bits)
    
    # Sumar 1 al complemento a 1
    complemento2 = list(complemento1)
    carry = 1
    for i in range(len(complemento2) - 1, -1, -1):
        if complemento2[i] == '1' and carry == 1:
            complemento2[i] = '0'
        elif complemento2[i] == '0' and carry == 1:
            complemento2[i] = '1'
            carry = 0
    
    return ''.join(complemento2)

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
    # Ignorar el bit de signo si es BCS
    if signo_mantisa:
        mantisa = cadena_bits[1:cant_bits_mantisa]
    else:
        mantisa = cadena_bits[:cant_bits_mantisa]

    # Agregar el bit implícito
    bit_implicito = '0.1'
    mantisa_con_bit_implicito = bit_implicito + mantisa

    # Convertir la mantisa a un valor decimal
    valor_mantisa = 0
    for i, bit in enumerate(mantisa_con_bit_implicito[2:], 1):  # Ignorar '0.'
        if bit == '1':
            valor_mantisa += 2 ** -i

    # Convertir el exponente a decimal
    valor_exponente = convertir_exponente_decimal(cadena_bits[cant_bits_mantisa:], signo_exponente, tipo_exponente)
    
    # Calcular la representación en punto flotante
    base = 2
    resultado = valor_mantisa * (base ** valor_exponente)

    # Si la mantisa es BCS, el resultado debe ser negativo
    if signo_mantisa:
        resultado = -resultado

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


# FUNCIONES DE CONVERSION DE CODIGOS BCD
def decimal_to_bcd(decimal_str):
    integer_part, _, decimal_part = decimal_str.partition('.')
    bcd = ''.join(format(int(d), '04b') for d in integer_part)
    if decimal_part:
        bcd += '.' + ''.join(format(int(d), '04b') for d in decimal_part)
    return bcd

def decimal_to_bcd_2421(decimal_str):
    mapping = {'0': '0000', '1': '0001', '2': '0010', '3': '0011',
               '4': '0100', '5': '1011', '6': '1100', '7': '1101',
               '8': '1110', '9': '1111'}
    integer_part, _, decimal_part = decimal_str.partition('.')
    bcd = ''.join(mapping[d] for d in integer_part)
    if decimal_part:
        bcd += '.' + ''.join(mapping[d] for d in decimal_part)
    return bcd

def decimal_to_bcd_exc3(decimal_str):
    integer_part, _, decimal_part = decimal_str.partition('.')
    bcd = ''.join(format(int(d) + 3, '04b') for d in integer_part)
    if decimal_part:
        bcd += '.' + ''.join(format(int(d) + 3, '04b') for d in decimal_part)
    return bcd

def decimal_to_bcd_8421(decimal_str):
    mapping = {'0': '0000', '1': '0001', '2': '0010', '3': '0011',
               '4': '0100', '5': '0101', '6': '0110', '7': '0111',
               '8': '1000', '9': '1001'}
    integer_part, _, decimal_part = decimal_str.partition('.')
    bcd = ''.join(mapping[d] for d in integer_part)
    if decimal_part:
        bcd += '.' + ''.join(mapping[d] for d in decimal_part)
    return bcd

def decimal_to_bcd_5421(decimal_str):
    mapping = {'0': '0000', '1': '0001', '2': '0010', '3': '0011',
               '4': '0100', '5': '1000', '6': '1001', '7': '1010',
               '8': '1011', '9': '1100'}
    integer_part, _, decimal_part = decimal_str.partition('.')
    bcd = ''.join(mapping[d] for d in integer_part)
    if decimal_part:
        bcd += '.' + ''.join(mapping[d] for d in decimal_part)
    return bcd

def print_bcd_table(decimal_str):
    print(f"Decimal: {decimal_str}")
    print(f"BCD:                {decimal_to_bcd(decimal_str)}")
    print(f"BCD 2421:           {decimal_to_bcd_2421(decimal_str)}")
    print(f"BCD EXC3:           {decimal_to_bcd_exc3(decimal_str)}")
    print(f"BCD 8421:           {decimal_to_bcd_8421(decimal_str)}")
    print(f"BCD 5421:           {decimal_to_bcd_5421(decimal_str)}")
    print()

# FUNCIONES DE CONVERSION DE CODIGOS GRAY Y JOHNSON

def binary_to_gray(binary):
    return binary[0] + ''.join(str(int(binary[i]) ^ int(binary[i+1])) for i in range(len(binary)-1))

def decimal_to_gray(decimal, bits):
    binary = decimal_to_binary(decimal, bits)
    gray = binary_to_gray(binary)
    return gray

def decimal_to_johnson(decimal, bits):
    if decimal >= 2 * bits:
        raise ValueError(f"El número decimal {decimal} es demasiado grande para {bits} bits en código Johnson")
    
    if decimal < bits:
        return '0' * (bits - decimal) + '1' * decimal
    else:
        return '1' * (2 * bits - decimal) + '0' * (decimal - bits)

# FUNCIONES DE CONVERSION IEEE754


def calcular_exponente_real(num):
    binary_representation = decimal_fraccionario_a_binario_fraccionario(num)
    punto_decimal = binary_representation.index('.')
    first_one_index = binary_representation.index('1')
    if first_one_index < punto_decimal:
        return punto_decimal - first_one_index - 1
    else:
        return punto_decimal - first_one_index

def normalizar_binario(num):
    binary_representation = decimal_fraccionario_a_binario_fraccionario(num)
    punto_decimal = binary_representation.index('.')
    first_one_index = binary_representation.index('1')
    
    normalized = binary_representation.replace('.', '')
    normalized = normalized[first_one_index:] + '0' * first_one_index
    normalized = normalized[:1] + '.' + normalized[1:]
    
    return normalized

def obtener_mantisa(binario_normalizado):
    fraccionaria = binario_normalizado.split('.')[1]
    mantisa = fraccionaria.ljust(23, '0')[:23]
    return mantisa

def calcular_exponente(num):
    exponente_real = calcular_exponente_real(num)
    exponente = exponente_real + 127
    return exponente

def determinar_bit_de_signo(num):
    return 1 if num < 0 else 0



def obtener_punto_flotante_IEEE754(num):
    signo = determinar_bit_de_signo(num)
    exponente = calcular_exponente(num)
    mantisa = obtener_mantisa(normalizar_binario(num))
    exponente_binario = f"{exponente:08b}"
    punto_flotante_binario = f"{signo}{exponente_binario}{mantisa}"
    return punto_flotante_binario

def imprimir_representaciones(binario):
    octal = oct(int(binario, 2))
    hexadecimal = hex(int(binario, 2))
    print("\nRepresentaciones en norma IEEE754 :")
    print(f"Binario: {binario}")
    print(f"Octal: {octal}")
    print(f"Hexadecimal: {hexadecimal}")

def ieee754_to_decimal(ieee754_str):
    sign = int(ieee754_str[0])
    exponent = int(ieee754_str[1:9], 2)
    fraction = ieee754_str[9:]

    real_exponent = exponent - 127

    decimal_fraction = 1.0
    for i, bit in enumerate(fraction):
        if bit == '1':
            decimal_fraction += 2 ** -(i + 1)

    result = (-1) ** sign * decimal_fraction * (2 ** real_exponent)

    return result


# FUNCIONES DE CONVERSION DE DECIMAL A C1, C2 Y SyM

def es_valido_SyM_o_C1(decimal, bits):
    # Calcular el rango de Signo y Magnitud (SyM)
    rango_min = -2**(bits - 1) + 1
    rango_max = 2**(bits - 1) - 1
    
    # Verificar si el decimal está dentro del rango
    if rango_min <= decimal <= rango_max:
        return 1
    else:
        return 0

def es_valido_Ca2(decimal, bits):
    # Calcular el rango de Complemento a 2 (Ca2)
    rango_min = -2**(bits - 1)
    rango_max = 2**(bits - 1) - 1
    
    # Verificar si el decimal está dentro del rango
    if rango_min <= decimal <= rango_max:
        return 1
    else:
        return 0

def decimal_a_complemento_a_1(decimal, bits):
    rango_min = -2**(bits - 1) + 1
    rango_max = 2**(bits - 1) - 1
    if es_valido_SyM_o_C1(decimal, bits):
        binario = decimal_to_binario(abs(decimal), bits)
        if decimal < 0:
            # Invertir los bits para obtener el complemento a 1
            complemento_a_1 = ''.join('1' if bit == '0' else '0' for bit in binario)
        else:
            complemento_a_1 = binario
        print(f"El número {decimal} en complemento a 1 es: {complemento_a_1}")
        print(f"El rango es: ({rango_min}, {rango_max})")
    else:
        print(f"El número {decimal} está fuera del rango ({rango_min}, {rango_max})")

def decimal_a_complemento_a_2(decimal, bits):
    rango_min = -2**(bits - 1)
    rango_max = 2**(bits - 1) - 1
    if es_valido_Ca2(decimal, bits):
        binario = decimal_to_binario(abs(decimal), bits)
        if decimal < 0:
            # Invertir los bits para obtener el complemento a 1
            complemento_a_1 = ''.join('1' if bit == '0' else '0' for bit in binario)
            # Sumar 1 para obtener el complemento a 2
            complemento_a_2 = bin(int(complemento_a_1, 2) + 1)[2:]
            # Asegurarse de que el resultado tenga la longitud correcta
            complemento_a_2 = complemento_a_2.zfill(bits)
        else:
            complemento_a_2 = binario
        print(f"El número {decimal} en complemento a 2 es: {complemento_a_2}")
        print(f"El rango es: ({rango_min}, {rango_max})")
    else:

        print(f"El número {decimal} está fuera del rango ({rango_min}, {rango_max})")


def is_positive(decimal):
    return decimal >= 0

def add_sign_bit(binary):
    return '0' + binary


def determine_bits(decimal):
    abs_decimal = abs(decimal)
    if abs_decimal < 128:
        return 8
    elif abs_decimal < 32768:
        return 16
    elif abs_decimal < 2147483648:
        return 32
    else:
        raise ValueError("El número es demasiado grande para ser representado en 32 bits.")


def complemento_a_1_sin_rango(binary):
    return ''.join('1' if bit == '0' else '0' for bit in binary)

def complemento_a_2_sin_rango(binary):
    comp_a_1 = complemento_a_1_sin_rango(binary)
    comp_a_2 = bin(int(comp_a_1, 2) + 1)[2:]
    return comp_a_2.zfill(len(binary))

def decimal_to_c1_c2(decimal):
    bits = determine_bits(decimal)
    binary = decimal_to_binary(decimal, bits)
    
    if decimal < 0:
        c1 = complemento_a_1_sin_rango(binary)
        c2 = complemento_a_2_sin_rango(binary)
        return bits, binary, c1, c2
    else:
        return bits, binary, None, None


def decimal_to_complemento_a_1(decimal, bits):
    binary = decimal_to_binary(abs(decimal), bits)
    if is_positive(decimal):
        return complemento_a_1_sin_rango(binary)
    else:
        signed_binary = add_sign_bit(binary)
        return complemento_a_1_sin_rango(signed_binary)
    
def complemento_a_2_sin_rango(binary):
    # Convertir el binario a complemento a 1
    comp_a_1 = complemento_a_1_sin_rango(binary)
    # Sumar 1 al complemento a 1
    comp_a_2 = bin(int(comp_a_1, 2) + 1)[2:]
    # Asegurarse de que el resultado tenga la misma longitud que el binario original
    return comp_a_2.zfill(len(binary))


def decimal_a_signo_y_magnitud(decimal, bits):
    rango_min = -2**(bits - 1) + 1
    rango_max = 2**(bits - 1) - 1
    if es_valido_SyM_o_C1(decimal, bits):
        binario = decimal_to_binario(abs(decimal), bits - 1)
        if decimal < 0:
            signo_y_magnitud = '1' + binario
        else:
            signo_y_magnitud = '0' + binario
        print(f"El número {decimal} en signo y magnitud es: {signo_y_magnitud}")
        print(f"El rango es: ({rango_min}, {rango_max})")
    else:

        print(f"El número {decimal} está fuera del rango ({rango_min}, {rango_max})")


# FUNCIONES DE CALCULADORA BINARIA

def obtener_entrada_binaria(mensaje, longitud_bits):
    while True:
        binario = input(mensaje)
        if len(binario) == longitud_bits and all(bit in '01' for bit in binario):
            return binario
        print(f"Entrada inválida. Por favor, ingrese un número binario de {longitud_bits} bits.")

def binario_a_decimal(binario, es_complemento_a_dos):
    if es_complemento_a_dos and binario[0] == '1':
        return int(binario, 2) - (1 << len(binario))
    return int(binario, 2)

def decimal_a_binario(decimal, longitud_bits, es_complemento_a_dos):
    if es_complemento_a_dos and decimal < 0:
        return format((1 << longitud_bits) + decimal, f'0{longitud_bits}b')
    return format(decimal & ((1 << longitud_bits) - 1), f'0{longitud_bits}b')

def calcular_banderas(a, b, resultado, longitud_bits, operacion):
    acarreo = int(resultado >= (1 << longitud_bits))
    cero = int(resultado == 0)
    negativo = int(resultado & (1 << (longitud_bits - 1)) != 0)
    
    signo_a = (a >> (longitud_bits - 1)) & 1
    signo_b = (b >> (longitud_bits - 1)) & 1
    signo_resultado = (resultado >> (longitud_bits - 1)) & 1
    
    if operacion == '+':
        desbordamiento = int((signo_a == signo_b) and (signo_resultado != signo_a))
    else:  # operacion == '-'
        desbordamiento = int((signo_a != signo_b) and (signo_resultado != signo_a))
    
    return acarreo, cero, negativo, desbordamiento


# FUNCIONES DE MENU
def bcd_conversion():
    while True:
        try:
            decimal_str = input("\nIngrese un número decimal para convertir (o 'q' para salir): ")
            if decimal_str.lower() == 'q':
                clear_screen()
                break
            float(decimal_str)  # Verificar si es un número válido
            if float(decimal_str) < 0:
                raise ValueError("El número debe ser positivo")
            print_bcd_table(decimal_str)
        except ValueError as e:
            print(f"Error: {e}. Por favor, ingrese un número decimal positivo válido.")

def gray_conversion():
    while True:
        try:
            bits = input("\nIngrese la cantidad de bits para el código Gray (o 'q' para volver al menú principal): ")
            if bits.lower() == 'q':
                clear_screen()
                break
            bits = int(bits)
            if bits <= 0:
                raise ValueError("La cantidad de bits debe ser positiva")
            
            decimal = input("Ingrese un número decimal para convertir a código Gray: ")
            decimal = int(decimal)
            if decimal < 0:
                raise ValueError("El número debe ser positivo")
            
            gray_code = decimal_to_gray(decimal, bits)
            print(f"El código Gray de {decimal} con {bits} bits es: {gray_code}")
        except ValueError as e:
            print(f"Error: {e}. Por favor, ingrese valores válidos.")

def johnson_conversion():
    while True:
        try:
            bits = input("\nIngrese la cantidad de bits para el código Johnson (o 'q' para volver al menú principal): ")
            if bits.lower() == 'q':
                clear_screen()
                break
            bits = int(bits)
            if bits <= 0:
                raise ValueError("La cantidad de bits debe ser positiva")
            
            decimal = input("Ingrese un número decimal para convertir a código Johnson: ")
            decimal = int(decimal)
            if decimal < 0:
                raise ValueError("El número debe ser positivo")
            
            johnson_code = decimal_to_johnson(decimal, bits)
            print(f"El código Johnson de {decimal} con {bits} bits es: {johnson_code}")
        except ValueError as e:
            print(f"Error: {e}. Por favor, ingrese valores válidos.")

def decimal_to_ieee754_conversion():
    while True:
        try:
            num = input("\nIngrese un número decimal para convertir a IEEE754 (o 'q' para volver al menú principal): ")
            if num.lower() == 'q':
                clear_screen()
                break
            num = float(num)
            
            binario_normalizado = normalizar_binario(num)
            mantisa = obtener_mantisa(binario_normalizado)
            exponente = calcular_exponente(num)
            signo = determinar_bit_de_signo(num)
            punto_flotante = obtener_punto_flotante_IEEE754(num)

            print("\nDatos del número en punto flotante:")
            print(f'Número ingresado: {num}')
            print(f'Representación binaria: {decimal_fraccionario_a_binario_fraccionario(num)}')
            print(f'Binario normalizado: {binario_normalizado}')
            print(f'Mantisa: {mantisa}')
            print(f'Exponente: {exponente}')
            print(f'Bit de signo: {signo}')
            imprimir_representaciones(punto_flotante)
        except ValueError as e:
            print(f"Error: {e}. Por favor, ingrese un número decimal válido.")

def ieee754_to_decimal_conversion():
    while True:
        print("\nConversor de IEEE 754 de 32 bits a decimal")
        ieee754_input = input("Ingrese el número en formato binario (32 bits) (o 'q' para volver al menú principal): ")
        
        if ieee754_input.lower() == 'q':
            clear_screen()
            break

        if len(ieee754_input) != 32 or not all(bit in '01' for bit in ieee754_input):
            print("Error: Por favor ingrese un número binario de 32 bits válido.")
            continue

        decimal_result = ieee754_to_decimal(ieee754_input)
        print(f"\nEl número decimal equivalente es: {decimal_result}")


def cadena_bits_a_punto_flotante():
    clear_screen()
    while True:
        print("\nConversor de cadena de bits a punto flotante")
        cadena_bits = input("Ingrese la cadena de bits (o 'q' para volver al menú principal): ")
        
        if cadena_bits.lower() == 'q':
            clear_screen()
            break

        if not es_cadena_bits_valida(cadena_bits):
            print("Error: Cadena de bits no válida. Por favor, ingrese solo '0' y '1'.")
            continue

        try:
            cant_bits_mantisa = obtener_cant_bits_mantisa_valida(cadena_bits)
            cant_bits_exponente = calcular_bits_exponente(cadena_bits, cant_bits_mantisa)
            signo_mantisa = obtener_signo_mantisa()
            signo_exponente = obtener_signo_exponente()
            tipo_mantisa = obtener_tipo_mantisa()
            tipo_exponente = obtener_tipo_exponente()

            rep_punto_flotante = calcular_representacion_de_pto_flotante(
                cadena_bits[:cant_bits_mantisa], 
                cadena_bits[cant_bits_mantisa:], 
                signo_mantisa, 
                signo_exponente, 
                tipo_mantisa, 
                tipo_exponente
            )
            print(f"\nRepresentación en punto flotante: {rep_punto_flotante}")

            rep_punto_flotante_fraccionaria = calcular_representacion_de_pto_flotante_con_mantisa_fraccionaria(
                cadena_bits, 
                cant_bits_mantisa, 
                signo_mantisa, 
                signo_exponente, 
                tipo_exponente
            )
            print(f"Representación en punto flotante con mantisa fraccionaria: {rep_punto_flotante_fraccionaria}")

            imprimir_si_mantisa_fraccionaria_normalizada(cadena_bits[:cant_bits_mantisa], signo_mantisa)

            mantisa_con_bit_implicito = agregar_bit_implicito(cadena_bits[:cant_bits_mantisa])
            rep_punto_flotante_con_bit_implicito = calcular_representacion_de_pto_flotante_con_mantisa_fraccionaria_con_bit_implicito(
                mantisa_con_bit_implicito, 
                cadena_bits, 
                cant_bits_mantisa, 
                signo_mantisa, 
                signo_exponente, 
                tipo_exponente
            )
            print(f"Representación en punto flotante con mantisa con bit implícito: {rep_punto_flotante_con_bit_implicito}")

        except ValueError as e:
            print(f"Error: {e}")

    

def es_cadena_bits_valida(cadena_bits):
    # Implementa la validación de la cadena de bits aquí
    return all(bit in '01' for bit in cadena_bits)



def menu_C1_C2_SM():
    while True:
        decimal_input = input("\nIngrese un número decimal (o 'Q' para terminar): ").strip()
        if decimal_input.upper() == 'Q':
            clear_screen()
            break
        try:
            decimal = int(decimal_input)
            bits = int(input("Ingrese la cantidad de bits: "))
        except ValueError:
            print("Entrada no válida. Intente nuevamente.")
            continue

        print("\nSeleccione el tipo de conversión: C1 - Complemento a 1 - C2 - Complemento a 2 - SM - Signo y Magnitud")
        opcion = input("Ingrese su opción (C1, C2, SM) o 'Q' para terminar: ").strip().upper()

        if opcion == 'C1':
            decimal_a_complemento_a_1(decimal, bits)
            print()
        elif opcion == 'C2':
            decimal_a_complemento_a_2(decimal, bits)
            print()
        elif opcion == 'SM':
            decimal_a_signo_y_magnitud(decimal, bits)
            print()
        elif opcion == 'Q':
            clear_screen()
            break
        else:
            print("Opción no válida. Intente nuevamente.")

def menu_C1_C2_sin_rango():
    while True:
        decimal_input = input("\nIngrese un número decimal (o 'Q' para terminar): ").strip()
        if decimal_input.upper() == 'Q':
            clear_screen()
            break
        try:
            decimal = int(decimal_input)
            bits, binary, c1, c2 = decimal_to_c1_c2(decimal)
            
            print(f"\nNúmero: {decimal}")
            print(f"Representación en {bits} bits:")
            print(f"Binario natural: {binary}")
            
            if decimal < 0:
                print("\nSeleccione el tipo de conversión:")
                print("1 - Complemento a 1")
                print("2 - Complemento a 2")
                opcion = input("Ingrese su opción (1, 2) o 'Q' para terminar: ").strip().upper()
                
                if opcion == '1':
                    print(f"Complemento a 1: {c1}")
                elif opcion == '2':
                    print(f"Complemento a 2: {c2}")
                elif opcion == 'Q':
                    break
                else:
                    print("Opción no válida. Volviendo al menú principal.")
            else:
                print("Nota: Un número positivo tiene la misma representación en binario natural para Complemento a 1 o Complemento a 2.")
            
            print()  # Línea en blanco para mejor legibilidad
            
        except ValueError as e:
            print(f"Error: {e}")

MAX_BITS = 32  # Define the maximum limit for the number of bits

def menu_calculadora_binaria():
    while True:
        try:
            # Validate number of bits input
            longitud_bits = input("\nIngrese el número de bits para la representación (o 'q' para volver al menú principal): ")
            if longitud_bits.lower() == 'q':
                clear_screen()
                break
            if not longitud_bits.isdigit() or int(longitud_bits) <= 0 or int(longitud_bits) > MAX_BITS:
                raise ValueError(f"El número de bits debe ser un entero positivo y no mayor a {MAX_BITS}.")
            longitud_bits = int(longitud_bits)
            
            es_complemento_a_dos = input("¿Está en complemento a dos? (s/n): ").lower()
            if es_complemento_a_dos not in ['s', 'n']:
                raise ValueError("Debe ingresar 's' para sí o 'n' para no.")
            es_complemento_a_dos = es_complemento_a_dos == 's'
            
            # Validate binary input
            a_binario = obtener_entrada_binaria(f"Ingrese el primer número binario de {longitud_bits} bits: ", longitud_bits)
            b_binario = obtener_entrada_binaria(f"Ingrese el segundo número binario de {longitud_bits} bits: ", longitud_bits)
            
            # Validate operation input
            operacion = input("Ingrese la operación (+ para suma, - para resta): ")
            if operacion not in ['+', '-']:
                raise ValueError("Operación inválida. Por favor ingrese + o -.")
            
            a = binario_a_decimal(a_binario, es_complemento_a_dos)
            b = binario_a_decimal(b_binario, es_complemento_a_dos)
            
            if operacion == '+':
                resultado = a + b
            else:
                resultado = a - b
            
            resultado_binario = decimal_a_binario(resultado, longitud_bits, es_complemento_a_dos)
            acarreo, cero, negativo, desbordamiento = calcular_banderas(a, b, resultado, longitud_bits, operacion)
            
            print(f"\nOperación: {a_binario} {operacion} {b_binario}")
            print(f"Resultado: {resultado_binario}")
            print(f"Resultado decimal: {binario_a_decimal(resultado_binario, es_complemento_a_dos)}")
            print("\nBanderas:")
            print(f"Acarreo (C): {acarreo}")
            print(f"Cero (Z): {cero}")
            print(f"Negativo (N): {negativo}")
            print(f"Desbordamiento (V): {desbordamiento}")
            
            continuar = input("\n¿Desea realizar otra operación? (s/n): ").lower()
            if continuar != 's':
                clear_screen()
                break
        except ValueError as ve:
            print(f"Entrada no válida: {ve}")
        except Exception as e:
            print(f"Error: {e}")

# FUNCION MENU PRINCIPAL

def main_menu():
    clear_screen()
    while True:
        print("\n--- menuManager.py (sistemas de computacion 1) ---")
        print("1. Conversión a códigos BCD")
        print("2. Conversión a código Gray")
        print("3. Conversión a código Johnson")
        print("4. Conversión de decimal a IEEE754 32 bits")
        print("5. Conversión de IEEE754 32 bits a decimal")
        print("6. Conversión de cadena de bits a representacion punto flotante")
        print("7. Conversión de decimal a C1, C2 y SyM con cantidad de bits específica")
        print("8. Conversión de decimal a C1, C2 sin cantidad de bits específica")
        print("9. Calculadora binaria con muestreo de flags")
        print("10. Salir")
        
        choice = input("Seleccione una opción (1-10): ")
        
        if choice == '1':
            clear_screen()
            bcd_conversion()
        elif choice == '2':
            clear_screen()
            gray_conversion()
        elif choice == '3':
            clear_screen()
            johnson_conversion()
        elif choice == '4':
            clear_screen()
            decimal_to_ieee754_conversion()
        elif choice == '5':
            clear_screen()
            ieee754_to_decimal_conversion()
        elif choice == '6':
            cadena_bits_a_punto_flotante()
        elif choice == '7':
            clear_screen()
            menu_C1_C2_SM()
        elif choice == '8':
            clear_screen()
            menu_C1_C2_sin_rango()
        elif choice == '9':
            clear_screen()
            menu_calculadora_binaria()
        elif choice == '10':
            clear_screen()
            print("Gracias por usar el programa. ¡Hasta luego!")
            print("Presione Enter para salir...")
            input()
            sys.exit(0)
        else:
            print("Opción no válida. Por favor, seleccione una opción del 1 al 7.")
            print("Presione Enter para continuar...")
            input()
            clear_screen()

if __name__ == "__main__":
    print("Bienvenido al programa de conversión de códigos")
    main_menu()


