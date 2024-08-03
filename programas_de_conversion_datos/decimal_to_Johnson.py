# pasaje de un numero decimal a código Johnson

def decimal_to_johnson(decimal, bits):
    if decimal >= 2 * bits:
        raise ValueError(f"El número decimal {decimal} es demasiado grande para {bits} bits en código Johnson")
    
    if decimal < bits:
        return '0' * (bits - decimal) + '1' * decimal
    else:
        return '1' * (2 * bits - decimal) + '0' * (decimal - bits)


cant_bits = int(input('Ingrese la cantidad de bits: '))
num = int(input('Ingrese un número decimal: '))

codigo_johnson = decimal_to_johnson(num, cant_bits)
print(f"El código Johnson de {num} con {cant_bits} bits es: {codigo_johnson}")