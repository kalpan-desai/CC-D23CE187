#include <stdio.h>
#include <ctype.h>
#include <string.h>

#define MAX_TOKEN_LEN 100

const char *keywords[] = {
    "auto", "break", "case", "char", "const", "continue", "default", "do", "double", "else", "enum",
    "extern", "float", "for", "goto", "if", "inline", "int", "long", "register", "restrict", "return",
    "short", "signed", "sizeof", "static", "struct", "switch", "typedef", "union", "unsigned", "void",
    "volatile", "while"
};

int keywordCount = 0, identifierCount = 0, integerCount = 0, floatCount = 0, charCount = 0;
int stringCount = 0, operatorCount = 0, punctuationCount = 0, mismatchCount = 0;

int isKeyword(const char *word) {
    for (int i = 0; i < sizeof(keywords) / sizeof(keywords[0]); i++) {
        if (strcmp(word, keywords[i]) == 0)
            return 1;
    }
    return 0;
}

void printToken(const char *token, const char *category) {
    printf("%-20s : %s\n", token, category);
}

void getNextToken(FILE *file) {
    char ch;
    char token[MAX_TOKEN_LEN];
    int idx = 0;

    while ((ch = fgetc(file)) != EOF && isspace(ch));
    if (ch == EOF) return;

    if (isalpha(ch) || ch == '_') {
        token[idx++] = ch;
        while ((ch = fgetc(file)) != EOF && (isalnum(ch) || ch == '_')) {
            token[idx++] = ch;
        }
        token[idx] = '\0';
        if (isKeyword(token)) {
            printToken(token, "KEYWORD");
            keywordCount++;
        } else {
            printToken(token, "IDENTIFIER");
            identifierCount++;
        }
        ungetc(ch, file);
    } else if (isdigit(ch)) {
        token[idx++] = ch;
        while ((ch = fgetc(file)) != EOF && isdigit(ch)) {
            token[idx++] = ch;
        }
        if (ch == '.') {
            token[idx++] = ch;
            while ((ch = fgetc(file)) != EOF && isdigit(ch)) {
                token[idx++] = ch;
            }
            printToken(token, "FLOAT LITERAL");
            floatCount++;
        } else {
            token[idx] = '\0';
            printToken(token, "INTEGER LITERAL");
            integerCount++;
        }
        ungetc(ch, file);
    } else if (ch == '\'') {
        token[idx++] = ch;
        ch = fgetc(file);
        token[idx++] = ch;
        ch = fgetc(file);
        if (ch == '\'') {
            token[idx++] = ch;
            token[idx] = '\0';
            printToken(token, "CHARACTER LITERAL");
            charCount++;
        } else {
            ungetc(ch, file);
        }
    } else if (ch == '"') {
        token[idx++] = ch;
        while ((ch = fgetc(file)) != EOF && ch != '"') {
            token[idx++] = ch;
        }
        token[idx++] = '"';
        token[idx] = '\0';
        printToken(token, "STRING LITERAL");
        stringCount++;
    } else if (strchr("+-*/=><!&|%^(){}[];,.:", ch)) {
        token[0] = ch;
        token[1] = '\0';
        printToken(token, "OPERATOR / PUNCTUATION");
        operatorCount++;
    } else {
        token[0] = ch;
        token[1] = '\0';
        printToken(token, "MISMATCH TOKEN");
        mismatchCount++;
    }
}

void lexicalAnalysis(const char *filename) {
    FILE *file = fopen(filename, "r");
    if (file == NULL) {
        printf("Error opening file: %s\n", filename);
        return;
    }

    printf("Tokenized Output:\n");
    while (!feof(file)) {
        getNextToken(file);
    }

    fclose(file);

    printf("\nSummary of Tokens:\n");
    printf("Keywords: %d\n", keywordCount);
    printf("Identifiers: %d\n", identifierCount);
    printf("Integer Literals: %d\n", integerCount);
    printf("Float Literals: %d\n", floatCount);
    printf("Character Literals: %d\n", charCount);
    printf("String Literals: %d\n", stringCount);
    printf("Operators / Punctuation: %d\n", operatorCount);
    printf("Mismatched Tokens: %d\n", mismatchCount);
}

int main() {
    const char *filename = "lex_check.c"; 
    lexicalAnalysis(filename);
    return 0;
}