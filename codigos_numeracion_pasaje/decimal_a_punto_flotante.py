# programa que pasa un numero decimal a punto flotante

def calcular_exponente_real(num):
    binary_representation = decimal_a_binario(num)
    punto_decimal = binary_representation.index('.')
    first_one_index = binary_representation.index('1')
    if first_one_index < punto_decimal:
        return punto_decimal - first_one_index - 1
    else:
        return punto_decimal - first_one_index

def normalizar_binario(num):
    binary_representation = decimal_a_binario(num)
    punto_decimal = binary_representation.index('.')
    first_one_index = binary_representation.index('1')
    
    # Eliminar el punto decimal y mover el primer '1' a la izquierda
    normalized = binary_representation.replace('.', '')
    normalized = normalized[first_one_index:] + '0' * first_one_index
    
    # Insertar el punto decimal después del primer dígito
    normalized = normalized[:1] + '.' + normalized[1:]
    
    return normalized

def obtener_mantisa(binario_normalizado):
    # Tomar la parte fraccionaria del número binario normalizado (sin el 1 implícito)
    fraccionaria = binario_normalizado.split('.')[1]
    
    # Rellenar con ceros hasta obtener 23 bits
    mantisa = fraccionaria.ljust(23, '0')[:23]
    return mantisa

def calcular_exponente(num):
    exponente_real = calcular_exponente_real(num)
    exponente = exponente_real + 127
    return exponente

def determinar_bit_de_signo(num):
    return 1 if num < 0 else 0

def decimal_a_binario(num):
    if num == 0:
        return "0.0"
    
    signo = '-' if num < 0 else ''
    num = abs(num)
    entero, decimal = str(num).split('.')
    entero = int(entero)
    decimal = float("0." + decimal)
    
    # Convertir la parte entera
    binario_entero = bin(entero)[2:]
    
    # Convertir la parte decimal
    binario_decimal = ""
    precision = 23  # Ajusta esto según la precisión que necesites
    while decimal > 0 and len(binario_decimal) < precision:
        decimal *= 2
        if decimal >= 1:
            binario_decimal += "1"
            decimal -= 1
        else:
            binario_decimal += "0"
    
    return f"{signo}{binario_entero}.{binario_decimal}"

def obtener_punto_flotante_IEEE754(num):
    # Obtener el bit de signo
    signo = determinar_bit_de_signo(num)
    
    # Calcular el exponente
    exponente = calcular_exponente(num)
    
    # Obtener la mantisa
    mantisa = obtener_mantisa(normalizar_binario(num))
    
    # Asegurarse de que el exponente tenga 8 bits
    exponente_binario = f"{exponente:08b}"
    
    # Combinar los componentes
    punto_flotante_binario = f"{signo}{exponente_binario}{mantisa}"
    
    return punto_flotante_binario

def imprimir_representaciones(binario):
    octal = oct(int(binario, 2))
    hexadecimal = hex(int(binario, 2))
    print()
    print("Representaciones en norma IEEE754 :")
    print(f"Binario: {binario}")
    print(f"Octal: {octal}")
    print(f"Hexadecimal: {hexadecimal}")

# programa principal

num = float(input('Ingrese un número decimal: '))
binario_normalizado = normalizar_binario(num)
mantisa = obtener_mantisa(binario_normalizado)
exponente = calcular_exponente(num)
signo = determinar_bit_de_signo(num)
punto_flotante = obtener_punto_flotante_IEEE754(num)

print("\nDatos del número en punto flotante:")
print(f'Número ingresado: {num}')
print(f'Representación binaria: {decimal_a_binario(num)}')
print(f'Binario normalizado: {binario_normalizado}')
print(f'Mantisa: {mantisa}')
print(f'Exponente: {exponente}')
print(f'Bit de signo: {signo}')
imprimir_representaciones(punto_flotante)