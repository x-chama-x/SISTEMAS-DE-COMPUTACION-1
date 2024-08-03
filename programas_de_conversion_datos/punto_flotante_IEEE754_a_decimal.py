def ieee754_to_decimal(ieee754_str):
    # Extraer las partes del número IEEE 754
    sign = int(ieee754_str[0])
    exponent = int(ieee754_str[1:9], 2)
    fraction = ieee754_str[9:]

    # Calcular el valor real del exponente
    real_exponent = exponent - 127

    # Convertir la fracción a decimal
    decimal_fraction = 1.0  # 1 implícito
    for i, bit in enumerate(fraction):
        if bit == '1':
            decimal_fraction += 2 ** -(i + 1)

    # Calcular el número final
    result = (-1) ** sign * decimal_fraction * (2 ** real_exponent)

    return result

def main():
    print("Conversor de IEEE 754 de 32 bits a decimal")
    print("Ingrese el número en formato binario (32 bits):")
    ieee754_input = input().strip()

    # Validar la entrada
    if len(ieee754_input) != 32 or not all(bit in '01' for bit in ieee754_input):
        print("Error: Por favor ingrese un número binario de 32 bits válido.")
        return

    decimal_result = ieee754_to_decimal(ieee754_input)
    print(f"\nEl número decimal equivalente es: {decimal_result}")

if __name__ == "__main__":
    main()