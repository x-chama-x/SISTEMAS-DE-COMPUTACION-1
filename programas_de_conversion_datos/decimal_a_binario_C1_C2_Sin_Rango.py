# Programa que convierte un número decimal negativo a binario en complemento a 1 y complemento a 2 con empaquetado automático

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

def decimal_to_binary(decimal, bits):
    return format(abs(decimal), f'0{bits}b')

def complemento_a_1_sin_rango(binary):
    return ''.join('1' if bit == '0' else '0' for bit in binary)

def complemento_a_2_sin_rango(binary):
    comp_a_1 = complemento_a_1_sin_rango(binary)
    comp_a_2 = bin(int(comp_a_1, 2) + 1)[2:]
    return comp_a_2.zfill(len(binary))

def decimal_to_c1_c2(decimal):
    if decimal >= 0:
        raise ValueError("Solo se aceptan números negativos para la conversión a C1 y C2.")
    
    bits = determine_bits(decimal)
    binary = decimal_to_binary(decimal, bits)
    
    c1 = complemento_a_1_sin_rango(binary)
    c2 = complemento_a_2_sin_rango(binary)
    
    return bits, binary, c1, c2

def menu():
    while True:
        decimal_input = input("Ingrese un número decimal negativo (o 'Q' para terminar): ").strip()
        if decimal_input.upper() == 'Q':
            break
        try:
            decimal = int(decimal_input)
            if decimal >= 0:
                print("Error: Solo se aceptan números negativos.")
                continue
            
            bits, binary, c1, c2 = decimal_to_c1_c2(decimal)
            
            print(f"\nNúmero: {decimal}")
            print(f"Representación en {bits} bits:")
            print(f"Binario natural: {binary}")
            
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
            
            print()  # Línea en blanco para mejor legibilidad
            
        except ValueError as e:
            print(f"Error: {e}")

# Llamar a la función menu para ejecutar el programa
menu()