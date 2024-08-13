# programa que convierte un número decimal a binario en complemento a 1 y complemento a 2 sin cantidad de bits fija

def decimal_to_binary(decimal, bits):
    return format(decimal, f'0{bits}b')

def is_positive(decimal):
    return decimal >= 0

def add_sign_bit(binary):
    return '0' + binary

def complemento_a_1_sin_rango(binary):
    return ''.join('1' if bit == '0' else '0' for bit in binary)

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


def menu():
    while True:
        decimal_input = input("Ingrese un número decimal (o 'Q' para terminar): ").strip()
        if decimal_input.upper() == 'Q':
            break
        try:
            decimal = int(decimal_input)
        except ValueError:
            print("Entrada no válida. Intente nuevamente.")
            continue

        print("\nSeleccione el tipo de conversión:")
        print("1 - Complemento a 1")
        print("2 - Complemento a 2")
        opcion = input("Ingrese su opción (1, 2) o 'Q' para terminar: ").strip().upper()

        if opcion == '1':
            resultado = decimal_to_complemento_a_1(decimal, 0)
            print(f"El numero {decimal} en complemento a 1 es: {resultado}\n")
        elif opcion == '2':
            binary = decimal_to_binary(abs(decimal), 0)
            if not is_positive(decimal):
                binary = add_sign_bit(binary)
            resultado = complemento_a_2_sin_rango(binary)
            print(f"El numero {decimal} en complemento a 2 es: {resultado}\n")
        elif opcion == 'Q':
            break
        else:
            print("Opción no válida. Intente nuevamente.")

# Llamar a la función menu para ejecutar el programa
menu()