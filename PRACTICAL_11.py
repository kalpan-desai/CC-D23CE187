import re

def generate_quadruples(expression):
    tokens = re.findall(r'\d+|[-+*/()]', expression.replace(' ', ''))
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    output, operators, quadruples = [], [], []
    temp_count = 1
    
    def process_operator():
        nonlocal temp_count
        op = operators.pop()
        b = output.pop()
        a = output.pop()
        temp_var = f't{temp_count}'
        quadruples.append((op, a, b, temp_var))
        output.append(temp_var)
        temp_count += 1
    
    for token in tokens:
        if token.isdigit():
            output.append(token)
        elif token in precedence:
            while (operators and operators[-1] in precedence and
                   precedence[operators[-1]] >= precedence[token]):
                process_operator()
            operators.append(token)
        elif token == '(':
            operators.append(token)
        elif token == ')':
            while operators and operators[-1] != '(':
                process_operator()
            operators.pop()
    
    while operators:
        process_operator()
    
    print("Operator | Operand1 | Operand2 | Result")
    for op, a, b, res in quadruples:
        print(f"{op:<9} | {a:<8} | {b:<8} | {res:<6}")

# Example usage
expression = input("Enter an expression: ")
generate_quadruples(expression)
