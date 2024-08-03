# pasaje de un numero decimal a todos los códigos BCDs posibles

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


def print_table(decimal):
    print(f"Decimal: {decimal}")
    print(f"BCD:                {decimal_to_bcd(decimal)}")
    print(f"BCD 2421:           {decimal_to_bcd_2421(decimal)}")
    print(f"BCD EXC3:           {decimal_to_bcd_exc3(decimal)}")
    print(f"BCD 3421:           {decimal_to_bcd_3421(decimal)}")
    print(f"BCD 5421:           {decimal_to_bcd_5421(decimal)}")
    print(f"BCD Empaquetado:    {decimal_to_packed_bcd(decimal)}")
    print()


while True:
    try:
        decimal = input("\nIngrese un número decimal para convertir (o 'q' para salir): ")
        if decimal.lower() == 'q':
            break
        decimal = int(decimal)
        if decimal < 0:
            raise ValueError("El número debe ser positivo")
        print_table(decimal)
    except ValueError as e:
        print(f"Error: {e}. Por favor, ingrese un número decimal positivo válido.")