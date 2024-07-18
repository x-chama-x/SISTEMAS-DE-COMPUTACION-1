#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <wchar.h>
#include <locale.h>

#define MAX_SYMBOLS 256
#define MAX_CODE_LENGTH 20

typedef struct {
    wchar_t symbol;
    int frequency;
    char code[MAX_CODE_LENGTH];
} Symbol;

void countFrequencies(const wchar_t *text, Symbol symbols[], int *symbolCount) {
    int frequencies[MAX_SYMBOLS] = {0};
    int length = wcslen(text);
    
    for (int i = 0; i < length; i++) {
        if (text[i] < MAX_SYMBOLS) {
            frequencies[text[i]]++;
        }
    }
    
    *symbolCount = 0;
    for (int i = 0; i < MAX_SYMBOLS; i++) {
        if (frequencies[i] > 0) {
            symbols[*symbolCount].symbol = (wchar_t)i;
            symbols[*symbolCount].frequency = frequencies[i];
            (*symbolCount)++;
        }
    }
}

int compareSymbols(const void *a, const void *b) {
    return ((Symbol *)b)->frequency - ((Symbol *)a)->frequency;
}

void shannonFano(Symbol symbols[], int start, int end, char *code) {
    if (start == end) {
        strcpy(symbols[start].code, code);
        return;
    }
    
    int totalFreq = 0;
    for (int i = start; i <= end; i++) {
        totalFreq += symbols[i].frequency;
    }
    
    int halfFreq = 0;
    int mid = start;
    while (mid <= end && halfFreq < totalFreq / 2) {
        halfFreq += symbols[mid].frequency;
        mid++;
    }
    mid--;
    
    char leftCode[MAX_CODE_LENGTH], rightCode[MAX_CODE_LENGTH];
    strcpy(leftCode, code);
    strcpy(rightCode, code);
    strcat(leftCode, "0");
    strcat(rightCode, "1");
    
    shannonFano(symbols, start, mid, leftCode);
    shannonFano(symbols, mid + 1, end, rightCode);
}

void printSymbol(wchar_t symbol) {
    switch(symbol) {
        case L' ':
            printf("(espacio)");
            break;
        case L'\n':
            printf("(salto de linea)");
            break;
        default:
            printf("%lc", symbol);
    }
}

int main() {
    setlocale(LC_ALL, "");  // Configurar la localización para manejar caracteres Unicode

    const wchar_t *text = L"un toque por si las moscas van\nvan van\notro toque por si vas detrás\nya no hay tiempo de lamentos\nno mas";
    Symbol symbols[MAX_SYMBOLS];
    int symbolCount = 0;
    
    countFrequencies(text, symbols, &symbolCount);
    qsort(symbols, symbolCount, sizeof(Symbol), compareSymbols);
    
    char initialCode[MAX_CODE_LENGTH] = "";
    shannonFano(symbols, 0, symbolCount - 1, initialCode);
    
    printf("Symbol\t\tFrequency\tShannon-Fano Code\n");
    for (int i = 0; i < symbolCount; i++) {
        printSymbol(symbols[i].symbol);
        printf("\t\t%d\t\t%s\n", symbols[i].frequency, symbols[i].code);
    }
    
    printf("\nTotal de simbolos unicos: %d\n", symbolCount);
    
    return 0;
}