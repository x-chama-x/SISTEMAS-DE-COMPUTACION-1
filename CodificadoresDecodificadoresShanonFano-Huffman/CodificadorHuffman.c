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
} HuffmanCode;

const char* find_code(HuffmanCode* codes, int num_codes, unsigned char symbol) {
    for (int i = 0; i < num_codes; i++) {
        if (codes[i].symbol == symbol) {
            return codes[i].code;
        }
    }
    return NULL;
}

void encode_line(const unsigned char* line, HuffmanCode* codes, int num_codes, char* encoded_output) {
    char temp[MAX_TOTAL_LENGTH] = "";
    for (int i = 0; line[i] != '\0'; i++) {
        const char* code = find_code(codes, num_codes, line[i]);
        if (code) {
            strcat(temp, code);
        } else {
            char not_found[50];
            sprintf(not_found, "Symbol not found: %02X ", line[i]);
            strcat(temp, not_found);
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
    HuffmanCode codes[] = {
        {' ', "111"},
        {'a', "001"},
        {0xA0, "1001011"},  // á en Windows-1252
        {'i', "10001"},
        {'e', "0111"},
        {'n', "1010"},
        {'o', "010"},
        {'s', "000"},
        {'t', "0110"},
        {'r', "11000"},
        {'u', "10011"},
        {'v', "10110"},
        {'m', "11001"},
        {'p', "10000"},
        {'l', "110111"},
        {'q', "110110"},
        {'y', "110101"},
        {'d', "110100"},
        {'h', "100100"},
        {'c', "1001010"},
        {'\n', "10111"}
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