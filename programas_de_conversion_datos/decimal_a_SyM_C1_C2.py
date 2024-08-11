# programa que convierte un número decimal a sistema de numeración SyM, Ca1 y Ca2

import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def decimal_a_binario(decimal, bits):
    # Convertir el número decimal a binario y eliminar el prefijo '0b'
    binario = bin(decimal)[2:]
    # Rellenar con ceros a la izquierda para asegurar la cantidad de bits
    binario = binario.zfill(bits)
    return binario

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
        binario = decimal_a_binario(abs(decimal), bits)
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
        binario = decimal_a_binario(abs(decimal), bits)
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


def decimal_a_signo_y_magnitud(decimal, bits):
    rango_min = -2**(bits - 1) + 1
    rango_max = 2**(bits - 1) - 1
    if es_valido_SyM_o_C1(decimal, bits):
        binario = decimal_a_binario(abs(decimal), bits - 1)
        if decimal < 0:
            signo_y_magnitud = '1' + binario
        else:
            signo_y_magnitud = '0' + binario
        print(f"El número {decimal} en signo y magnitud es: {signo_y_magnitud}")
        print(f"El rango es: ({rango_min}, {rango_max})")
    else:

        print(f"El número {decimal} está fuera del rango ({rango_min}, {rango_max})")


def menu_C1_C2_SM():
    while True:
        decimal_input = input("Ingrese un número decimal (o 'Q' para terminar): ").strip()
        if decimal_input.upper() == 'Q':
            break
        try:
            decimal = int(decimal_input)
            bits = int(input("Ingrese la cantidad de bits: "))
        except ValueError:
            print("Entrada no válida. Intente nuevamente.")
            continue

        print("\nSeleccione el tipo de conversión:")
        print("C1 - Complemento a 1")
        print("C2 - Complemento a 2")
        print("SM - Signo y Magnitud")
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
            break
        else:
            print("Opción no válida. Intente nuevamente.")


# Llamada al menú principal
menu_C1_C2_SM()