# Conversión de un número decimal (incluyendo fracciones) a todos los códigos BCDs posibles

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

def decimal_to_bcd_3421(decimal_str):
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

def decimal_to_packed_bcd(decimal_str):
    integer_part, _, decimal_part = decimal_str.partition('.')
    if len(integer_part) % 2 != 0:
        integer_part = '0' + integer_part
    packed = ''
    for i in range(0, len(integer_part), 2):
        packed += format(int(integer_part[i]), '04b') + format(int(integer_part[i+1]), '04b')
    if decimal_part:
        if len(decimal_part) % 2 != 0:
            decimal_part += '0'
        packed += '.'
        for i in range(0, len(decimal_part), 2):
            packed += format(int(decimal_part[i]), '04b') + format(int(decimal_part[i+1]), '04b')
    return packed

def print_table(decimal_str):
    print(f"Decimal: {decimal_str}")
    print(f"BCD:                {decimal_to_bcd(decimal_str)}")
    print(f"BCD 2421:           {decimal_to_bcd_2421(decimal_str)}")
    print(f"BCD EXC3:           {decimal_to_bcd_exc3(decimal_str)}")
    print(f"BCD 3421:           {decimal_to_bcd_3421(decimal_str)}")
    print(f"BCD 5421:           {decimal_to_bcd_5421(decimal_str)}")
    print(f"BCD Empaquetado:    {decimal_to_packed_bcd(decimal_str)}")
    print()

while True:
    try:
        decimal_str = input("\nIngrese un número decimal para convertir (o 'q' para salir): ")
        if decimal_str.lower() == 'q':
            break
        float(decimal_str)  # Verificar si es un número válido
        if float(decimal_str) < 0:
            raise ValueError("El número debe ser positivo")
        print_table(decimal_str)
    except ValueError as e:
        print(f"Error: {e}. Por favor, ingrese un número decimal positivo válido.")