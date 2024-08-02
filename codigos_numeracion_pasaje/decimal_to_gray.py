# pasaje de un numero decimal a código Gray 

def decimal_to_binary(decimal, bits):
    return format(decimal, f'0{bits}b')

def binary_to_gray(binary):
    return binary[0] + ''.join(str(int(binary[i]) ^ int(binary[i+1])) for i in range(len(binary)-1))

def decimal_to_gray(decimal, bits):
    binary = decimal_to_binary(decimal, bits)
    gray = binary_to_gray(binary)
    return gray

cant_bits = int(input('Ingrese la cantidad de bits: '))
num = int(input('Ingrese un número decimal: '))

codigo_gray = decimal_to_gray(num, cant_bits)
print(f"El código Gray de {num} con {cant_bits} bits es: {codigo_gray}")

