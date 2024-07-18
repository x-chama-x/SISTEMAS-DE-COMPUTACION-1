#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAX_SYMBOLS 256
#define MAX_CODE_LENGTH 20
#define MAX_TOTAL_LENGTH 10000

typedef struct {
    unsigned char symbol;
    char code[MAX_CODE_LENGTH];
} HuffmanCode;

typedef struct Node {
    unsigned char symbol;
    struct Node* left;
    struct Node* right;
} Node;

Node* create_node() {
    Node* node = (Node*)malloc(sizeof(Node));
    node->symbol = '\0';
    node->left = NULL;
    node->right = NULL;
    return node;
}

void build_tree(Node* root, HuffmanCode* codes, int num_codes) {
    for (int i = 0; i < num_codes; i++) {
        Node* current = root;
        for (int j = 0; codes[i].code[j] != '\0'; j++) {
            if (codes[i].code[j] == '0') {
                if (!current->left) current->left = create_node();
                current = current->left;
            } else {
                if (!current->right) current->right = create_node();
                current = current->right;
            }
        }
        current->symbol = codes[i].symbol;
    }
}

void decode(Node* root, const char* encoded, char* decoded) {
    Node* current = root;
    char* output = decoded;
    
    while (*encoded) {
        if (*encoded == '0') {
            current = current->left;
        } else {
            current = current->right;
        }
        
        if (current->symbol != '\0') {
            *output++ = current->symbol;
            current = root;
        }
        encoded++;
    }
    *output = '\0';
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

    Node* root = create_node();
    build_tree(root, codes, num_codes);

    char encoded[MAX_TOTAL_LENGTH];
    char decoded[MAX_TOTAL_LENGTH];

    printf("Ingrese la cadena binaria codificada:\n");
    fgets(encoded, sizeof(encoded), stdin);
    encoded[strcspn(encoded, "\n")] = 0;  // Eliminar el salto de línea final

    decode(root, encoded, decoded);

    printf("\nTexto decodificado:\n");
    for (int i = 0; decoded[i] != '\0'; i++) {
        if (decoded[i] == '\n') {
            printf("\\n");  // Imprimir "\n" para los saltos de línea
        } else if (decoded[i] == 0xA0) {
            printf("á");    // Manejar específicamente el carácter 'á'
        } else {
            printf("%c", decoded[i]);
        }
    }
    printf("\n");

    return 0;
}