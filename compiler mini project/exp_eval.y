%{
#include <stdio.h>
#include <stdlib.h>

int yylex();
void yyerror(const char *s);
double result;  // Store the final result
%}

%union {
    double dval;
}

%token <dval> NUMBER

%left '+' '-'
%left '*' '/'
%left '(' ')'

%type <dval> expr

%%

input:
      expr '\n' { result = $1; printf("Result: %.2f\n", result); exit(0); }
    | '\n'      { /* Ignore empty lines */ }
    ;

expr:
      expr '+' expr { $$ = $1 + $3; }
    | expr '-' expr { $$ = $1 - $3; }
    | expr '*' expr { $$ = $1 * $3; }
    | expr '/' expr { 
        if ($3 == 0) {
            yyerror("Division by zero!");
            exit(1);
        }
        $$ = $1 / $3; 
    }
    | '(' expr ')'  { $$ = $2; }
    | NUMBER        { $$ = $1; }
    ;

%%

void yyerror(const char *s) {
    printf("Error: %s\n", s);
}

int main() {
    printf("Enter an arithmetic expression: ");
    yyparse();
    return 0;
}
