# Define the grammar as productions
grammar = {
    'S': [['A', 'B', 'C'], ['D']],
    'A': [['a'], ['ε']],
    'B': [['b'], ['ε']],
    'C': [['(', 'S', ')'], ['c']],
    'D': [['A', 'C']]
}

# Function to calculate First set
def first(symbol, first_sets):
    if symbol not in grammar:  # If symbol is terminal
        return {symbol}
    
    if symbol in first_sets:  # If First set is already computed for symbol
        return first_sets[symbol]
    
    first_set = set()
    for production in grammar.get(symbol, []):
        if production == ['ε']:
            first_set.add('ε')
        else:
            for char in production:
                first_set |= first(char, first_sets)
                if 'ε' not in first_set:
                    break
    first_sets[symbol] = first_set
    return first_set

# Function to calculate Follow set
def follow(symbol, follow_sets, first_sets, start_symbol='S'):
    if symbol in follow_sets:
        return follow_sets[symbol]
    
    follow_set = set()
    
    if symbol == start_symbol:
        follow_set.add('$')  # End of input symbol
    
    for non_terminal, productions in grammar.items():
        for production in productions:
            for i, char in enumerate(production):
                if char == symbol:
                    if i + 1 < len(production):
                        follow_set |= first(production[i+1], first_sets) - {'ε'}
                    if i + 1 == len(production) or 'ε' in first(production[i+1], first_sets):
                        follow_set |= follow(non_terminal, follow_sets, first_sets, start_symbol)
    
    follow_sets[symbol] = follow_set
    return follow_set

# Generate the First and Follow sets
def generate_first_and_follow():
    first_sets = {}
    follow_sets = {}
    
    for non_terminal in grammar:
        first(non_terminal, first_sets)
        follow(non_terminal, follow_sets, first_sets)
    
    return first_sets, follow_sets

# Construct the predictive parsing table
def construct_parsing_table(first_sets, follow_sets):
    parsing_table = {}
    for non_terminal in grammar:
        parsing_table[non_terminal] = {}
        for production in grammar[non_terminal]:
            if production == ['ε']:
                for terminal in follow_sets[non_terminal]:
                    parsing_table[non_terminal][terminal] = production
            else:
                for symbol in production:
                    if symbol != 'ε':
                        for terminal in first(symbol, first_sets):
                            if terminal != 'ε':
                                parsing_table[non_terminal][terminal] = production
    return parsing_table

# LL(1) Grammar Check
def is_ll1(parsing_table):
    for non_terminal in parsing_table:
        for terminal in parsing_table[non_terminal]:
            if terminal in parsing_table[non_terminal]:
                return False
    return True

# String validation using the parsing table
def validate_string(input_string, parsing_table, start_symbol='S'):
    stack = [start_symbol, '$']
    input_string = list(input_string) + ['$']
    
    while stack:
        top = stack.pop()
        current_symbol = input_string[0]
        
        if top == current_symbol:
            input_string.pop(0)
        elif top in grammar:
            production = parsing_table.get(top, {}).get(current_symbol)
            if production:
                stack.extend(reversed(production))
            else:
                return "Invalid string"
        else:
            return "Invalid string"
    
    return "Valid string" if not input_string else "Invalid string"

# Main program execution
def main(input_string):
    first_sets, follow_sets = generate_first_and_follow()
    parsing_table = construct_parsing_table(first_sets, follow_sets)
    
    print("First Sets:", first_sets)
    print("Follow Sets:", follow_sets)
    print("Parsing Table:", parsing_table)
    
    if is_ll1(parsing_table):
        print("Grammar is LL(1).")
        result = validate_string(input_string, parsing_table)
        print(result)
    else:
        print("Grammar is not LL(1).")

# Test cases
input_strings = ['abc', 'ac', '(abc)', 'c', '(ac)', 'a', '()', '(ab)', 'abcabc', 'b']
for input_string in input_strings:
    print(f"Validating string: {input_string}")
    main(input_string)
