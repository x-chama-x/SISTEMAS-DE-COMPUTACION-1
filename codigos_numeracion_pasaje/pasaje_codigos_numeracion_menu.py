import sys
import os

# Función para limpiar la pantalla
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Funciones de conversión
def decimal_to_bcd(decimal):
    return ''.join(format(int(d), '04b') for d in str(decimal))

def decimal_to_bcd_2421(decimal):
    mapping = {'0': '0000', '1': '0001', '2': '0010', '3': '0011',
               '4': '0100', '5': '1011', '6': '1100', '7': '1101',
               '8': '1110', '9': '1111'}
    return ''.join(mapping[d] for d in str(decimal))

def decimal_to_bcd_exc3(decimal):
    return ''.join(format(int(d) + 3, '04b') for d in str(decimal))

def decimal_to_bcd_3421(decimal):
    mapping = {'0': '0000', '1': '0001', '2': '0010', '3': '0011',
               '4': '0100', '5': '0101', '6': '0110', '7': '0111',
               '8': '1000', '9': '1001'}
    return ''.join(mapping[d] for d in str(decimal))

def decimal_to_bcd_5421(decimal):
    mapping = {'0': '0000', '1': '0001', '2': '0010', '3': '0011',
               '4': '0100', '5': '1000', '6': '1001', '7': '1010',
               '8': '1011', '9': '1100'}
    return ''.join(mapping[d] for d in str(decimal))

def decimal_to_packed_bcd(decimal):
    if len(str(decimal)) % 2 != 0:
        decimal = '0' + str(decimal)
    packed = ''
    for i in range(0, len(str(decimal)), 2):
        packed += format(int(str(decimal)[i]), '04b') + format(int(str(decimal)[i+1]), '04b')
    return packed

def print_bcd_table(decimal):
    print(f"Decimal: {decimal}")
    print(f"BCD:                {decimal_to_bcd(decimal)}")
    print(f"BCD 2421:           {decimal_to_bcd_2421(decimal)}")
    print(f"BCD EXC3:           {decimal_to_bcd_exc3(decimal)}")
    print(f"BCD 3421:           {decimal_to_bcd_3421(decimal)}")
    print(f"BCD 5421:           {decimal_to_bcd_5421(decimal)}")
    print(f"BCD Empaquetado:    {decimal_to_packed_bcd(decimal)}")

def decimal_to_binary(decimal, bits):
    return format(decimal, f'0{bits}b')

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

def decimal_a_binario(num):
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

# Funciones de menú
def bcd_conversion():
    while True:
        try:
            decimal = input("\nIngrese un número decimal para convertir a BCD (o 'q' para volver al menú principal): ")
            if decimal.lower() == 'q':
                clear_screen()
                break
            decimal = int(decimal)
            if decimal < 0:
                raise ValueError("El número debe ser positivo")
            print_bcd_table(decimal)
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
            print(f'Representación binaria: {decimal_a_binario(num)}')
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

def main_menu():
    clear_screen()
    while True:
        print("\n--- Menú Principal ---")
        print("1. Conversión a códigos BCD")
        print("2. Conversión a código Gray")
        print("3. Conversión a código Johnson")
        print("4. Conversión de decimal a IEEE754")
        print("5. Conversión de IEEE754 a decimal")
        print("6. Salir")
        
        choice = input("Seleccione una opción (1-6): ")
        
        if choice == '1':
            bcd_conversion()
        elif choice == '2':
            gray_conversion()
        elif choice == '3':
            johnson_conversion()
        elif choice == '4':
            decimal_to_ieee754_conversion()
        elif choice == '5':
            ieee754_to_decimal_conversion()
        elif choice == '6':
            print("Gracias por usar el programa. ¡Hasta luego!")
            sys.exit(0)
        else:
            print("Opción no válida. Por favor, seleccione una opción del 1 al 6.")

if __name__ == "__main__":
    print("Bienvenido al programa de conversión de códigos")
    main_menu()