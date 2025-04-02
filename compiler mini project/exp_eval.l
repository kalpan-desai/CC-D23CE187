%{
#include <stdio.h>
#include <stdlib.h>
#include "exp_eval.tab.h"
%}

%%

[0-9]+(\.[0-9]+)?  { 
    printf("Token: NUMBER, Value: %s\n", yytext); 
    yylval.dval = atof(yytext); 
    return NUMBER; 
}
[+\-*/()]          { 
    printf("Token: '%c'\n", yytext[0]); 
    return yytext[0]; 
}
[\n]               { 
    printf("Token: NEWLINE\n"); 
    return '\n'; 
}
[ \t]              { /* Ignore whitespace */ }
.                  { 
    printf("Invalid character: %s\n", yytext); 
}

%%

int yywrap() {
    return 1;
}
