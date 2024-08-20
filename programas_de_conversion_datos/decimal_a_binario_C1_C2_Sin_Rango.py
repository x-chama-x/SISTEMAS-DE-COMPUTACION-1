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
    binary = format(abs(decimal), f'b')
    if decimal < 0:
        binary = binary.zfill(bits)
    return binary

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

def menu():
    while True:
        decimal_input = input("Ingrese un número decimal (o 'Q' para terminar): ").strip()
        if decimal_input.upper() == 'Q':
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

# Llamar a la función menu para ejecutar el programa
menu()