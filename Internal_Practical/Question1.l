%{
    #include <stdio.h>
    #include <string.h>
    #include <ctype.h>    
%}

%%

\<p\>     { printf("%s is Paragraph tag\n", yytext); }
\<h1\>    { printf("%s is Heading tag\n", yytext); }
\<div\>   { printf("%s is Division tag\n", yytext); }
\<a\>     { printf("%s is Anchor tag\n", yytext); }
[a-zA-Z0-9 ]+   { printf("%s is Page Content\n", yytext); }

%%

int main() {
    yylex();
    return 0;
}

int yywrap() {
    return 1;
}
