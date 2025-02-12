%{
#include <stdio.h>
#include <ctype.h>
#include <string.h>

int word_count = 0;
int char_count = 0;
int letter_count = 0;
int line_count = 1;

int stop_flag = 0;
%}

%%

"{exit}"           { stop_flag = 1; return 0; }
[a-zA-Z]+        { word_count++; letter_count += yyleng; char_count += yyleng; }  
[0-9]+           { word_count++; char_count += yyleng; }
[ \t]+           { char_count += yyleng; }
\n              { char_count++; line_count++; }
.               { char_count++; }

%%

int main() {
    printf("Enter text (type '{exit}' to stop and display counts):\n");
    while (!stop_flag) {
        yylex();
    }

    printf("\nWords: %d\n", word_count);
    printf("Letters: %d\n", letter_count);
    printf("Characters: %d\n", char_count);
    printf("Lines: %d\n", line_count);
    return 0;
}

int yywrap() {
    return 1;
}
