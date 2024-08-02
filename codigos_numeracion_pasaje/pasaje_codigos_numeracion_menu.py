# programa que convierte un número decimal a los códigos BCD, Gray y Johnson

import sys

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

def bcd_conversion():
    while True:
        try:
            decimal = input("\nIngrese un número decimal para convertir a BCD (o 'q' para volver al menú principal): ")
            if decimal.lower() == 'q':
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

def main_menu():
    while True:
        print("\n--- Menú Principal ---")
        print("1. Conversión a códigos BCD")
        print("2. Conversión a código Gray")
        print("3. Conversión a código Johnson")
        print("4. Salir")
        
        choice = input("Seleccione una opción (1-4): ")
        
        if choice == '1':
            bcd_conversion()
        elif choice == '2':
            gray_conversion()
        elif choice == '3':
            johnson_conversion()
        elif choice == '4':
            print("Gracias por usar el programa. ¡Hasta luego!")
            sys.exit(0)
        else:
            print("Opción no válida. Por favor, seleccione una opción del 1 al 4.")

if __name__ == "__main__":
    print("Bienvenido al programa de conversión de códigos")
    main_menu()