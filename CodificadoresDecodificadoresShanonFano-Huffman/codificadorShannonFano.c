#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAX_SYMBOLS 256
#define MAX_CODE_LENGTH 20
#define MAX_LINE_LENGTH 1000
#define MAX_TOTAL_LENGTH 10000

typedef struct {
    unsigned char symbol;
    char code[MAX_CODE_LENGTH];
} ShannonFanoCode;

const char* find_code(ShannonFanoCode* codes, int num_codes, unsigned char symbol) {
    for (int i = 0; i < num_codes; i++) {
        if (codes[i].symbol == symbol) {
            return codes[i].code;
        }
    }
    return NULL;
}

void encode_line(const unsigned char* line, ShannonFanoCode* codes, int num_codes, char* encoded_output) {
    char temp[MAX_TOTAL_LENGTH] = "";
    for (int i = 0; line[i] != '\0'; i++) {
        const char* code = find_code(codes, num_codes, line[i]);
        if (code) {
            strcat(temp, code);
        } else {
            // Si no se encuentra el código, usar el código del espacio
            const char* space_code = find_code(codes, num_codes, ' ');
            if (space_code) {
                strcat(temp, space_code);
            }
        }
    }
    // Añadir el código para el salto de línea al final
    const char* newline_code = find_code(codes, num_codes, '\n');
    if (newline_code) {
        strcat(temp, newline_code);
    }
    strcat(encoded_output, temp);
}

int main() {
    ShannonFanoCode codes[] = {
        {' ', "000"},
        {'o', "001"},
        {'a', "0100"},
        {'s', "0101"},
        {'n', "011"},
        {'e', "1001"},
        {'t', "1000"},
        {'\n', "11000"},
        {'r', "10100"},
        {'v', "10101"},
        {'m', "1011"},
        {'u', "11011"},
        {'i', "11010"},
        {'p', "11001"},
        {'l', "11110"},
        {'q', "11101"},
        {'y', "111000"},
        {'d', "111001"},
        {'h', "111110"},
        {'c', "1111111"},
        {0xE1, "1111110"},  // á en UTF-8
        {0xA0, "1111110"},  // á en Windows-1252
        {0xC3, "1111110"},  // Primer byte de á en UTF-8 (en caso de que se lea byte por byte)
    };
    int num_codes = sizeof(codes) / sizeof(codes[0]);

    unsigned char line[MAX_LINE_LENGTH];
    char total_encoded[MAX_TOTAL_LENGTH] = "";
    int line_number = 1;

    printf("Ingrese el texto linea por linea (presione Enter dos veces para finalizar):\n");

    while (1) {
        if (fgets((char*)line, sizeof(line), stdin) == NULL || line[0] == '\n') {
            break;
        }

        // Eliminar el salto de línea al final si existe
        size_t len = strlen((char*)line);
        if (len > 0 && line[len-1] == '\n') {
            line[len-1] = '\0';
        }

        printf("Linea %d original: ", line_number);
        for (int i = 0; line[i] != '\0'; i++) {
            printf("%02X ", line[i]);
        }
        printf("\n");

        printf("Linea %d codificada: ", line_number);
        char encoded_line[MAX_TOTAL_LENGTH] = "";
        encode_line(line, codes, num_codes, encoded_line);
        printf("%s\n\n", encoded_line);

        strcat(total_encoded, encoded_line);
        line_number++;
    }

    printf("\nCodificacion completa en binario:\n%s\n", total_encoded);

    return 0;
}